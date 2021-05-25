from zendesk_search.cli import cli


def test_it_runs():
    assert cli() == True
