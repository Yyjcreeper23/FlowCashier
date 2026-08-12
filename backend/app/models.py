"""
Pydantic models to define the structure of data flowing in and out of the API.
Used in FastAPI to generate interactive /docs and validate incoming JSON.
"""

from datetime import date
from pydantic import BaseModel
from typing import List

class Transaction(BaseModel):
    name: str
    amount: float
    date: date
    recurring: bool = False

class ForecastRequest(BaseModel):
    starting_balance: float
    transactions: List[Transaction]
    month: str