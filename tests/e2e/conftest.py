import codecs
import errno
import os
import select
import time

import pytest
import regex
from ptyprocess import PtyProcess


def remove_ansi_escape_sequences(text):
    # http://stackoverflow.com/questions/14693701/how-can-i-remove-the-ansi-escape-sequences-from-a-string-in-python
    # remove all ansi escape sequences
    text = regex.sub(r"(\x9b|\x1b\[)[0-?]*[ -\/]*[@-~]", "", text)
    text = regex.sub(r"[ \r]*\n", "\n", text)  # also clean up the line endings
    return text


# Taken from:
# https://github.com/CITGuru/PyInquirer/blob/7637373429bec66788650cda8091b7a6f12929ee/tests/helpers.py
# Getting terminal output asserting working properly is tricky.
class SimplePty(PtyProcess):
    """Simple wrapper around a process running in a pseudoterminal.
    This class exposes a similar interface to :class:`PtyProcess`, but its read
    methods return unicode, and its :meth:`write` accepts unicode.
    """

    def __init__(self, pid, fd, encoding="utf-8", codec_errors="strict"):
        super(SimplePty, self).__init__(pid, fd)
        self.encoding = encoding
        self.codec_errors = codec_errors
        self.decoder = codecs.getincrementaldecoder(encoding)(errors=codec_errors)

    def read(self, size=1024):
        """Read at most ``size`` bytes from the pty, return them as unicode.
        Can block if there is nothing to read. Raises :exc:`EOFError` if the
        terminal was closed.
        The size argument still refers to bytes, not unicode code points.
        """
        b = super(SimplePty, self).read(size)
        if not b:
            return ""
        if self.skip_cr:
            b = b.replace(b"\r", b"")
        # if self.skip_ansi:
        #    b = remove_ansi_escape_sequences(b)
        return self.decoder.decode(b, final=False)

    def readline(self):
        """Read one line from the pseudoterminal, and return it as unicode.
        Can block if there is nothing to read. Raises :exc:`EOFError` if the
        terminal was closed.
        note: this is a specialized version that does not have \r\n at the end
        """
        # TODO implement a timeout
        b = super(SimplePty, self).readline().strip()
        s = self.decoder.decode(b, final=False)
        if self.skip_ansi:
            s = remove_ansi_escape_sequences(s)
        return s

    def write(self, s):
        """Write the unicode string ``s`` to the pseudoterminal.
        This intends to make tests a little less verbose.
        Returns the number of bytes written.
        """
        if isinstance(s, str):
            b = s.encode(self.encoding)
        count = super(SimplePty, self).write(b)
        return count

    def writeline(self, s):
        """Syntactic sugar to add a '\n' at the end of the .
        Returns the number of bytes written.
        """
        if not s.endswith("\n"):
            s += "\n"
        return self.write(s)

    @classmethod
    def spawn(
        cls,
        argv,
        cwd=None,
        env=None,
        echo=False,
        preexec_fn=None,
        dimensions=(24, 80),
        skip_cr=True,
        skip_ansi=True,
        timeout=1.0,
    ):
        """
        :param argv:
        :param cwd:
        :param env:
        :param echo: default is False so we do not have to deal with the echo
        :param preexec_fn:
        :param dimensions:
        :param skip_cr: skip carriage return '/r' characters when comparing equality
        :param skip_ansi: skip ansi escape sequences when comparing equality
        :param timeout: read timeout in seconds
        :return: subprocess handle
        """
        if env is None:
            env = os.environ
        inst = super(SimplePty, cls).spawn(argv, cwd, env, echo, preexec_fn, dimensions)
        inst.skip_cr = skip_cr
        inst.skip_ansi = skip_ansi
        inst.timeout = timeout  # in seconds
        return inst

    def expect(self, text, strict=True):
        """Read until equals text or timeout."""
        # inspired by pexpect/pty_spawn and  pexpect/expect.py expect_loop
        end_time = time.time() + self.timeout
        buf = ""
        while (end_time - time.time()) > 0.0:
            # switch to nonblocking read
            reads, _, _ = select.select([self.fd], [], [], end_time - time.time())
            if len(reads) > 0:
                try:
                    buf = remove_ansi_escape_sequences(buf + self.read())
                except EOFError:
                    print("len: %d" % len(buf))
                    if strict:
                        assert buf == text
                    else:
                        assert text in buf
                if buf == text:
                    return
                elif len(buf) >= len(text):
                    break
            else:
                # do not eat up CPU when waiting for the timeout to expire
                time.sleep(self.timeout / 10)
        # print(repr(buf))  # debug ansi code handling
        if strict:
            assert buf == text
        else:
            assert text in buf

    def expect_regex(self, pattern):
        """Read until matches pattern or timeout."""
        # inspired by pexpect/pty_spawn and  pexpect/expect.py expect_loop
        end_time = time.time() + self.timeout
        buf = ""
        prog = regex.compile(pattern)
        while (end_time - time.time()) > 0.0:
            # switch to nonblocking read
            reads, _, _ = select.select([self.fd], [], [], end_time - time.time())
            if len(reads) > 0:
                try:
                    buf = remove_ansi_escape_sequences(buf + self.read())
                except EOFError:
                    assert (
                        prog.match(buf) is not None
                    ), "output was:\n%s\nexpect regex pattern:\n%s" % (buf, pattern)
                if prog.match(buf):
                    return True
            else:
                # do not eat up CPU when waiting for the timeout to expire
                time.sleep(self.timeout / 10)
        assert (
            prog.match(buf) is not None
        ), "output was:\n%s\nexpect regex pattern:\n%s" % (buf, pattern)


@pytest.fixture
def cd_root(request):
    os.chdir(request.config.rootdir.strpath)
    yield
    os.chdir(request.config.invocation_dir)


@pytest.fixture
def cli_app(cd_root):
    app = SimplePty.spawn(
        ["python", "-m", "zendesk_search", "--show-banner=false", "-vvvvv"]
    )
    time.sleep(1)
    yield app
    # Ensure test coverage is gathered.
    time.sleep(app.delayafterterminate)
    try:
        # In case the subprocess wasn't cleaned up by the test.
        app.sendintr()
    except OSError as err:
        if err.errno != errno.EIO:
            raise
    # Make extra sure the child is getting cleaned up.
    # app.wait() can block if there is unread IO but the app has actually closed.
    app.terminate()
    app.wait()


@pytest.fixture
def keys():
    return {
        "up": "\x1b[A",
        "down": "\x1b[B",
        "right": "\x1b[C",
        "left": "\x1b[D",
        "enter": "\x0d",
    }
