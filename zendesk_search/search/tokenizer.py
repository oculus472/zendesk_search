import re


def tokenize(text: str) -> list[str]:
    """Transform a string into a list of tokens.
    This is done by removing punctuation and splitting by whitespace.

    Args:
        text (str): The text to tokenize.

    Returns:
        list[str]: A list of tokens (words) from the suppplied text.
    """
    text = re.sub(r"[^\w\s]", "", text)
    text = text.lower()
    return text.split()
