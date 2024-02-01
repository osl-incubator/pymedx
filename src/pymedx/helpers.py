"""Module for helper functions."""
from typing import Generator, List, Optional, Union
from xml.etree.ElementTree import Element


def batches(
    iterable: List[str], n: int = 1
) -> Generator[List[str], str, None]:
    """
    Create batches from an iterable.

    Parameters
    ----------
    iterable: Iterable
        the iterable to batch.
    n: Int
        the batch size.

    Returns
    -------
    batches: List
        yields batches of n objects taken from the iterable.
    """
    # Get the length of the iterable
    length = len(iterable)

    # Start a loop over the iterable
    for index in range(0, length, n):
        # Create a new iterable by slicing the original
        yield iterable[index : min(index + n, length)]


def getContent(
    element: Element,
    path: str,
    default: Optional[str] = None,
    separator: str = "\n",
) -> Union[str, None, int]:
    """
    Retrieve text content of an XML element.

    Parameters
    ----------
        - element   Element, the XML element to parse.
        - path      Str, Nested path in the XML element.
        - default   Str, default value to return when no text is found.

    Returns
    -------
        - text      Str, text in the XML node.
    """
    # Find the path in the element
    result = element.findall(path)

    # Return the default if there is no such element
    if result is None or len(result) == 0:
        return default

    # Extract the text and return it
    else:
        return separator.join(
            [sub.text for sub in result if sub.text is not None]
        )
