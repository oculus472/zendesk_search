import json


def display_document(document):
    """Prints the supplied document to the terminal

    Args:
        document (dict): document to display.
    """
    text = json.dumps(document, indent=4)
    print(text)
