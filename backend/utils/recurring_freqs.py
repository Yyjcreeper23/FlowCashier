from enum import Enum

class RecurringFrequency(str, Enum):
    """
    String Enum class representing how often something recurs.
    Within this project, this will be used to represent how often a transaction occurs.
    """
    ONE_TIME = "One Time"
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"
    YEARLY = "Yearly"