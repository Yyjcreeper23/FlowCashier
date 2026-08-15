"""
Forecast handling functions.
Responsible for computing forecasts based on provided transactions.
"""

import calendar
from datetime import date

from .models import ForecastRequest, ForecastResponse, Transaction
from utils.converters import from_date, to_recurring_freq
from utils.recurring_freqs import RecurringFrequency


def _occurs_on(transaction: Transaction, given_date: date) -> bool:
    """
    Checks if a transaction occurs on a given date.

    Attributes:
        transaction: The transaction to check.
        given_date: The date to check.

    Returns:
        True if the transaction occurs on the given date depending on its recurring_freq, False otherwise or when
        given an invalid recurring_freq.
    """
    freq = to_recurring_freq(transaction.recurring_freq) if isinstance(transaction.recurring_freq, str) else transaction.recurring_freq
    match freq:
        case RecurringFrequency.ONE_TIME:
            return transaction.date == given_date
        case RecurringFrequency.DAILY:
            return transaction.date <= given_date
        case RecurringFrequency.WEEKLY:
            return transaction.date <= given_date and transaction.date.weekday() == given_date.weekday()
        case RecurringFrequency.MONTHLY:
            return given_date.day == min(transaction.date.day, calendar.monthrange(given_date.year, given_date.month)[1])
        case RecurringFrequency.YEARLY:
            return transaction.date.month == given_date.month and given_date.day == min(transaction.date.day, calendar.monthrange(given_date.year, given_date.month)[1])
        case _:
            return False


def build_forecast(req: ForecastRequest) -> ForecastResponse:
    """
    Builds a forecast based on the provided request.

    Attributes:
        req: The request containing the required forecast parameters.

    Returns:
        The forecast response.
    """
    year, month = (int(part) for part in req.month.split("-"))
    days_in_month = calendar.monthrange(year, month)[1]

    running_balance = req.starting_balance
    balances: dict[str, float] = {}

    lowest_balance = float("inf")
    lowest_balance_date = from_date(date(year, month, 1))

    highest_balance = float("-inf")
    highest_balance_date = from_date(date(year, month, 1))

    for day_num in range(1, days_in_month + 1):
        current_day = date(year, month, day_num)

        day_total = sum(t.amount for t in req.transactions if _occurs_on(t, current_day))
        running_balance = round(running_balance + day_total, 2)
        balances[from_date(current_day)] = running_balance

        if running_balance < lowest_balance:
            lowest_balance = running_balance
            lowest_balance_date = from_date(current_day)
        
        if running_balance > highest_balance:
            highest_balance = running_balance
            highest_balance_date = from_date(current_day)

    return ForecastResponse(
        balances=balances,
        lowest_balance=lowest_balance,
        lowest_balance_date=lowest_balance_date,
        highest_balance=highest_balance,
        highest_balance_date=highest_balance_date,
        month=req.month
    )