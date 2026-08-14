from datetime import date
from app.models import Transaction
from utils.converters import to_date
from utils.recurring_freqs import RecurringFrequency


example_transactions = [
    Transaction(
        name="Salary",
        amount=4000.00,
        date=to_date("01-01-2026"),
        recurring_freq=RecurringFrequency.MONTHLY,
    ),
    Transaction(
        name="Rent",
        amount=-200.00,
        date=to_date("31-01-2026"),
        recurring_freq=RecurringFrequency.MONTHLY,
    ),
    Transaction(
        name="Food",
        amount=-40.00,
        date=to_date("01-01-2026"),
        recurring_freq=RecurringFrequency.DAILY,
    ),
    Transaction(
        name="Netflix",
        amount=-50.00,
        date=to_date("21-01-2026"),
        recurring_freq=RecurringFrequency.YEARLY,
    ),
]
