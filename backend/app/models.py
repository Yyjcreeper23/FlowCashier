from datetime import datetime
from utils.recurring_freqs import RecurringFrequency
from sqlmodel import Field, SQLModel


class TransactionBase(SQLModel):
    """
    SQLModel data model (Pydantic) used for creating a transaction through the API.
    The Base model Transaction others can inherit from.

    Attributes:
        name: String for identifying the transaction in a human readable manner
        amount: Float representing the amount of money involved in the transaction (positive for income, negative for expenses)
        date: DateTime object representing the date when the transaction occurred
        recurring_freq: RecurringFrequency object representing how often should the transaction recur
    """
    name: str = Field(index=True)
    amount: float  # Positive for income, negative for expenses
    date: datetime
    recurring_freq: RecurringFrequency = Field(default=RecurringFrequency.ONE_TIME, index=True)


class Transaction(TransactionBase, table=True):
    """
    SQLModel table model (Pydantic + SQLAlchemy) representing a transaction (that is, income or expenses).
    Inherits other attributes from TransactionBase.

    Attributes:
        tr_id: Int that acts as the primary key for each transaction in the table (can be initialised as None to let SQLModel auto-generate it instead)
    """
    tr_id: int | None = Field(default=None, primary_key=True)


class TransactionCreate(TransactionBase):
    """
    SQLModel data model (Pydantic) used for creating a transaction through the API.
    Will be used to define the data that we want to receive in the API when creating a new transaction.
    """
    pass


class TransactionPublic(TransactionBase):
    """
    SQLModel data model (Pydantic) used for reading a transaction through the API.
    A transaction read from the API will come from the database, in which the transaction will always have an id.

    Attributes:
        tr_id: Int that acts as the primary key for each transaction in the table
    """
    tr_id: int

class TransactionUpdate(SQLModel):
    """
    SQLModel data model (Pydantic) used for updating a transaction through the API.

    Attributes:
        name: String for identifying the transaction in a human readable manner, or None if no changes were made
        amount: Float representing the amount of money involved in the transaction (positive for income, negative for expenses), or None if no changes were made
        date: DateTime object representing the date when the transaction occurred, or None if no changes were made
        recurring_freq: RecurringFrequency object representing how often should the transaction recur, or None if no changes were made
    """
    name: str | None = None
    amount: float | None = None
    date: datetime | None = None
    recurring_freq: RecurringFrequency | None = None

# class ForecastRequest(BaseModel):
#     starting_balance: float
#     transactions: List[Transaction]
#     month: str