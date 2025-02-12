"""Module for helper functions."""

from __future__ import annotations

import datetime
import re

from typing import Generator, Optional, cast

import lxml.etree

from lxml.etree import _Element


def arrange_query(search_term, start_date, end_date):
    """
    Create a new query adding range date according PubMed format.

    Parameters
    ----------
    search_term : str
        term to search in PubMed database
    start_date : date
        Beginning of the range date.
    end_date : date
        Ending of the range date.

    Returns
    -------
    search query : str
        A new query to use in PubMed API.
    """
    date_filter = "Date - Publication"
    from_date = start_date.strftime("%Y/%m/%d")
    to_date = end_date.strftime("%Y/%m/%d")
    date_query = f'"{from_date}"[{date_filter}] : "{to_date}"[{date_filter}]'

    return f"({search_term}) AND ({date_query})"


def get_search_term(input_string: str) -> str:
    """
    Extract just the search term from a full query.

    by a full query is undertood a query with range date.

    Parameters
    ----------
    input_string : str
        A query with dates.

    Returns
    -------
    search term : str
        Isolated search term.

    Notes
    -----
    i.e.
    input_string:
    ('(virus AND bacteria) AND'
    ' ("2022/01/01"[Date - Publication] : "2023/12/01"[Date - Publication])')
    output:
    virus AND bacteria
    """
    # Regex pattern to match date ranges
    date_pattern = (
        r'AND\s*\(\s*"\d{4}/\d{2}/\d{2}"\s*\[Date - Publication\]\s*:'
        r'\s*"\d{4}/\d{2}/\d{2}"\s*\[Date - Publication\]\s*\)'
    )

    # Remove the date range
    cleaned_string = re.sub(date_pattern, "", input_string)

    # Ensure no extra spaces around the logical operators
    cleaned_string = re.sub(r"\s+", " ", cleaned_string).strip()

    # Remove leading and trailing parentheses if
    # they enclose the whole expression
    if cleaned_string.startswith("(") and cleaned_string.endswith(")"):
        cleaned_string = cleaned_string[1:-1]

    return cleaned_string.strip()


def get_range_months(
    start_date: datetime.date, end_date: datetime.date
) -> list[tuple[datetime.date, datetime.date]]:
    """
    Divide a range date into month ranges.

    Parameters
    ----------
    start_date: date
        Beginning of the range date.
    end_date: date
        Ending of the range date.

    Returns
    -------
    date_ranges: list[tuple[date, date]]
        A list of smaller range dates per month.

    Notes
    -----
    i.e. (in date python type)
    input: 2020-03-01 to 2020-05-15
    output:
        [(2020-03-01, 2020-03-31),
         (2020-04-01, 2020-04-30),
         (2020-05-01, 2020-05-15)]
    """
    MONTHS_IN_YEAR = 12
    date_ranges = []

    # Start at the first day of the starting month
    current_start_date = start_date

    while current_start_date <= end_date:
        # Calculate the end of the current month
        # i.e. current_start_date = 2020-03-01
        # Showing a simulation of how are changing the variables
        # next_month = 2020-03-29 + 000-00-04 = 2020-04-02
        # current_end_date = 2020-04-02 - 000-00-02 = 2020-03-31
        next_month = current_start_date.replace(day=28) + datetime.timedelta(
            days=4
        )
        current_end_date = next_month - datetime.timedelta(days=next_month.day)

        # Adjust the end date if it goes beyond the specified end_date
        current_end_date = min(current_end_date, end_date)

        date_ranges.append((current_start_date, current_end_date))

        # Move to the first day of next month
        if current_end_date.month == MONTHS_IN_YEAR:
            current_start_date = current_end_date.replace(
                year=current_end_date.year + 1, month=1, day=1
            )
        else:
            current_start_date = current_end_date.replace(
                month=current_end_date.month + 1, day=1
            )

    return date_ranges


def get_range_date_from_query(
    input_string: str,
) -> tuple[datetime.date, datetime.date] | None:
    """
    Extract the dates from a PubMed query.

    If there no range date return None.

    Parameters
    ----------
    input_string: str
        A PubMed query

    Returns
    -------
    date_ranges: tuple[date, date]
        A tuple with the start range date and end range date.

    Notes
    -----
    i.e.
    input_string:
    ('(virus AND bacteria) AND'
    ' ("2022/01/01"[Date - Publication] : "2023/12/01"[Date - Publication])')
    output:
    (date(2022/01/01), date(2023/12/01)
    """
    EXPECTED_DATES = 2
    # Regular expression to match the date pattern
    date_pattern = r'"(\d{4}/\d{2}/\d{2})"\[Date - Publication\]'

    # Find all matches of the date pattern in the input string
    matches = re.findall(date_pattern, input_string)

    # Convert the extracted date strings into datetime objects
    dates = [
        datetime.datetime.strptime(date, "%Y/%m/%d").date() for date in matches
    ]

    # Check if exists dates otherwise return None
    if len(dates) == EXPECTED_DATES:
        return (dates[0], dates[1])

    return None


def get_range_years(
    start_date: datetime.date, end_date: datetime.date
) -> list[tuple[datetime.date, datetime.date]]:
    """
    Divide a range date into year range.

    Parameters
    ----------
    start_date: date
        begining of the range date.
    end_date: date
        ending of the range date.

    Returns
    -------
    date_ranges: list[tuples[date, date]]
        a list of a smaller range dates per year.

    Notes
    -----
    i.e. date type

    input: 2020-03-01 to 2022-12-23

    output:
    [(2020-03-01, 2020-12-31),
    (2021-01-01, 2021-12-31),
    (2022-01-01, 2022-12-23)]
    """
    # Define the end of the starting year
    date_ranges = []

    end_of_first_year = datetime.datetime(start_date.year, 12, 31).date()

    if start_date <= end_of_first_year:
        # If the start date is before the end of the year, add this period
        # to the list
        date_ranges.append((start_date, min(end_of_first_year, end_date)))

    # Iterate over the full years between the start and end dates
    for year in range(start_date.year + 1, end_date.year):
        start_of_year = datetime.datetime(year, 1, 1).date()
        end_of_year = datetime.datetime(year, 12, 31).date()
        date_ranges.append((start_of_year, end_of_year))

    # Define the start of the ending year
    if end_date.year >= start_date.year:
        start_of_last_year = datetime.date(end_date.year, 1, 1)
        if start_of_last_year < end_date:
            date_ranges.append((start_of_last_year, end_date))

    return date_ranges


def batches(
    iterable: list[str], n: int = 1
) -> Generator[list[str], str, None]:
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
    element: _Element,
    path: str,
    default: Optional[str] = None,
    separator: str = "\n",
) -> Optional[str | int]:
    """
    Retrieve text content of an XML element.

    Parameters
    ----------
    element: Element
        the XML element to parse.
    path: Str
        Nested path in the XML element.
    default: Str
        default value to return when no text is found.

    Returns
    -------
    text: Str
        text in the XML node.
    """
    # Find the path in the element
    result = element.findall(path)

    # Return the default if there is no such element
    if result is None or len(result) == 0:
        return default

    # Extract the text and return it
    return separator.join([sub.text for sub in result if sub.text is not None])


def getContentUnique(
    element: _Element,
    path: str,
    default: Optional[str] = None,
) -> Optional[str | int]:
    """
    Retrieve text content of an XML element. Returns a unique value.

    Parameters
    ----------
    element: Element
        the XML element to parse.
    path: Str
        Nested path in the XML element.
    default: Str
        default value to return when no text is found.

    Returns
    -------
    text: Str
        text in the XML node.
    """
    # Find the path in the element
    result = cast(list[_Element], element.findall(path))

    # Return the default if there is no such element
    if not result:
        return default

    # Extract the text and return it
    return cast(str, result[0].text)


def getAllContent(
    element: _Element,
    path: str,
    default: Optional[str] = None,
) -> Optional[str | int]:
    """
    Retrieve text content of an XML element.

    Return all the text inside the path and omit XML tags inside.

    Parameters
    ----------
    element: Element
        the XML element to parse.
    path: Str
        Nested path in the XML element.
    default: Str
        default value to return when no text is found.

    Returns
    -------
    text: str
        text in the XML node.
    """
    # Find the path in the element
    raw_result = element.findall(path)

    # Return the default if there is no such element
    if not raw_result:
        return default

    # Get all text avoiding the tags
    result = cast(
        str,
        lxml.etree.tostring(
            raw_result[0], method="text", encoding="utf-8"
        ).decode("utf-8"),
    )

    # Extract the text and return it
    return " ".join(result.split())


def getAbstract(
    element: _Element,
    path: str,
    default: Optional[str] = None,
) -> Optional[str | int]:
    """
    Retrieve text content of an XML element.

    Return all the text inside the path and omit XML tags inside.
    and omits abstract-type == scanned-figures

    Parameters
    ----------
    element: Element
        the XML element to parse.
    path: Str
        Nested path in the XML element.
    default: Str
        default value to return when no text is found.

    Returns
    -------
    text: str
        text in the XML node.
    """
    # Find the path in the element
    raw_result = element.findall(path)

    # Return the default if there is no such element
    if not raw_result:
        return default

    if raw_result[0].attrib.get("abstract-type", None) == "scanned-figures":
        return default

    for fig in raw_result[0].iter("fig"):
        parent = fig.getparent()
        if parent is not None:
            parent.remove(fig)

    # Get all text avoiding the tags
    result = cast(
        str,
        lxml.etree.tostring(
            raw_result[0], method="text", encoding="utf-8"
        ).decode("utf-8"),
    )

    # Extract the text and return it
    return " ".join(result.split())
