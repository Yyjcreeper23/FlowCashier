from datetime import date as date_type  # prevents unresolvable annotation error, as Python resolves TransactionBase's date in the type annotation as the field itself, not the type
from pydantic import BaseModel
from sqlmodel import Field, SQLModel

from utils.constants import DEFAULT_TRANSACTION_NAME, DEFAULT_TRANSACTION_AMOUNT, DEFAULT_TRANSACTION_DATE, DEFAULT_TRANSACTION_RECURRING_FREQ, DEFAULT_FORECAST_STARTING_BALANCE, DEFAULT_FORECAST_MONTH_STR
from utils.recurring_freqs import RecurringFrequency


# ===========================================================================
# TRANSACTION MODELS
# ===========================================================================
class TransactionBase(SQLModel):
    """
    SQLModel data model (Pydantic) used for creating a transaction through the API.
    The Base model Transaction others can inherit from.

    Attributes:
        name: String for identifying the transaction in a human readable manner
        amount: Float representing the amount of money involved in the transaction (positive for income, negative for expenses)
        date: Date object representing the date when the transaction occurred
        recurring_freq: RecurringFrequency object representing how often should the transaction recur
    """
    name: str = Field(default=DEFAULT_TRANSACTION_NAME, index=True)
    amount: float = Field(default=DEFAULT_TRANSACTION_AMOUNT)
    date: date_type = Field(default=DEFAULT_TRANSACTION_DATE)
    recurring_freq: RecurringFrequency = Field(default=DEFAULT_TRANSACTION_RECURRING_FREQ, index=True)


class Transaction(TransactionBase, table=True):
    """
    SQLModel table model (Pydantic + SQLAlchemy) representing a transaction (that is, income or expenses).
    Inherits other attributes from TransactionBase.

    Attributes:
        tr_id: Int that acts as the primary key for each transaction in the table (can be initialised as None to let SQLModel auto-generate it instead)
        name: (Inherited from TransactionBase) String for identifying the transaction in a human readable manner
        amount: (Inherited from TransactionBase) Float representing the amount of money involved in the transaction (positive for income, negative for expenses)
        date: (Inherited from TransactionBase) Date object representing the date when the transaction occurred
        recurring_freq: (Inherited from TransactionBase) RecurringFrequency object representing how often should the transaction recur
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
        date: Date object representing the date when the transaction occurred, or None if no changes were made
        recurring_freq: RecurringFrequency object representing how often should the transaction recur, or None if no changes were made
    """
    name: str | None = None
    amount: float | None = None
    date: date_type | None = None
    recurring_freq: RecurringFrequency | None = None


# ===========================================================================
# FORECAST MODELS
# ===========================================================================
class ForecastRequest(BaseModel):
    """
    BaseModel used for a request of a forecast.

    Attributes:
        starting_balance: Float representing the starting balance of that month
        transactions: List of Transactions representing all transactions of that month
        month: String that represents the target month, format should be YYYY-MM, e.g. '2026-08'
    """
    starting_balance: float = Field(default=DEFAULT_FORECAST_STARTING_BALANCE)
    transactions: list[Transaction]
    month: str = Field(default=DEFAULT_FORECAST_MONTH_STR, description="Target month as YYYY-MM, e.g. '2026-08")


class ForecastResponse(BaseModel):
    """
    BaseModel used for a response of a forecast.

    Attributes:
        balances: Dictionary representing the projected balance at the end of each day in the month
        lowest_balance: Float representing the lowest balance during the month
        lowest_balance_date: String representing the date when the lowest balance occurred
        month: String representing the target month, format should be YYYY-MM, e.g. '2026-08'
    """
    balances: dict[str, float]
    lowest_balance: float
    lowest_balance_date: str
    month: str