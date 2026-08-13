from datetime import datetime
from app.models import Transaction, RecurringFrequency

transactions = [
    Transaction(
        name="Salary",
        amount=4000.00,
        date=datetime.strptime("01-01-2026", "%d-%m-%Y"),
        recurring_freq=RecurringFrequency.MONTHLY,
    ),
    Transaction(
        name="Rent",
        amount=-200.00,
        date=datetime.strptime("31-01-2026", "%d-%m-%Y"),
        recurring_freq=RecurringFrequency.MONTHLY,
    ),
    Transaction(
        name="Food",
        amount=-40.00,
        date=datetime.strptime("01-01-2026", "%d-%m-%Y"),
        recurring_freq=RecurringFrequency.DAILY,
    ),
    Transaction(
        name="Netflix",
        amount=-50.00,
        date=datetime.strptime("21-01-2026", "%d-%m-%Y"),
        recurring_freq=RecurringFrequency.YEARLY,
    ),
]
