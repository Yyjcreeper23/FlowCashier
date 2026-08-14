from datetime import date

from .constants import DATE_FORMAT, DEFAULT_DATE_ON_CONVERSION_FAIL, DEFAULT_DATE_STR_ON_CONVERSION_FAIL
from .recurring_freqs import RecurringFrequency


def to_date(input_str: str) -> date:
    """
    Converts a string to a date object. Case insensitive. Ignores leading and trailing whitespaces.

    Attributes:
        input_str: Input string, must ideally be of %d-%m-%Y aka DD-MM-YYYY format

    Returns:
        A date object parsed from input_str. DEFAULT_DATE by default if conversion is unsuccessful.
    """
    try:
        return date.strptime(input_str.lower().strip(), DATE_FORMAT)
    except:
        return DEFAULT_DATE_ON_CONVERSION_FAIL


def from_date(input_dt: date) -> str:
    """
    Converts a date object to a string.

    Attributes:
        input_dt: Input date object

    Returns:
        A string equal to input_dt's string value in DATE_FORMAT format. DEFAULT_DATE_STR by default if conversion is unsuccessful.
    """
    try:
        return date.strftime(input_dt, DATE_FORMAT)
    except:
        return DEFAULT_DATE_STR_ON_CONVERSION_FAIL


def to_recurring_freq(input_str: str) -> RecurringFrequency:
    """
    Converts a string to a RecurringFrequency object. Case insensitive. Ignores leading and trailing whitespaces.

    Attributes:
        input_str: Input string, must ideally be one of "One Time", "Daily", "Weekly", "Monthly", "Yearly"

    Returns:
        A RecurringFrequency object parsed from input_str. RecurringFrequency.ONE_TIME by default if parse is unsuccessful.
    """
    match input_str.lower().strip():
        case RecurringFrequency.ONE_TIME.value.lower():
            return RecurringFrequency.ONE_TIME
        case RecurringFrequency.DAILY.value.lower():
            return RecurringFrequency.DAILY
        case RecurringFrequency.WEEKLY.value.lower():
            return RecurringFrequency.WEEKLY
        case RecurringFrequency.MONTHLY.value.lower():
            return RecurringFrequency.MONTHLY
        case RecurringFrequency.YEARLY.value.lower():
            return RecurringFrequency.YEARLY
        case _:
            return RecurringFrequency.ONE_TIME


def from_recurring_freq(input_rf: RecurringFrequency) -> str:
    """
    Converts a RecurringFrequency to its string value.

    Attributes:
        input_rf: Input RecurringFrequency object

    Returns:
        A string equal to input_rf's string value. "One Time" by default.
    """
    match input_rf:
        case RecurringFrequency.ONE_TIME:
            return RecurringFrequency.ONE_TIME.value
        case RecurringFrequency.DAILY:
            return RecurringFrequency.DAILY.value
        case RecurringFrequency.WEEKLY:
            return RecurringFrequency.WEEKLY.value
        case RecurringFrequency.MONTHLY:
            return RecurringFrequency.MONTHLY.value
        case RecurringFrequency.YEARLY:
            return RecurringFrequency.YEARLY.value
        case _:
            return RecurringFrequency.ONE_TIME.value