from datetime import datetime
from enum import Enum
from sqlmodel import Field, SQLModel

class RecurringFrequency(Enum):
    ONE_TIME = "One Time"
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"
    YEARLY = "Yearly"

class Transaction(SQLModel, table=True):
    """
    SQLModel class representing a transaction (that is, income or expenses)

    Attributes:
        name: String for identifying the transaction in a human readable manner
        amount: Float representing the amount of money involved in the transaction (positive for income, negative for expenses)
        date: DateTime object representing the date when the transaction occurred
        recurring_freq: RecurringFrequency object representing how often should the transaction recur
    """
    id: int | None = Field(default=None, primary_key=True)
    name: str
    amount: float  # Positive for income, negative for expenses
    date: datetime
    recurring_freq: RecurringFrequency


# class ForecastRequest(BaseModel):
#     starting_balance: float
#     transactions: List[Transaction]
#     month: str
