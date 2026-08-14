from fastapi import APIRouter

from app.models import ForecastRequest, ForecastResponse
from app.forecast_builder import build_forecast


router = APIRouter(
    prefix="/api",
    tags=["forecast"]
)

# ===========================================================================
# CREATE METHODS
# ===========================================================================
@router.post("/forecast", response_model=ForecastResponse)
def forecast(req: ForecastRequest):
    """
    Builds a forecast based on the provided request.

    Attributes:
        req: The request containing the required forecast parameters.

    Returns:
        The forecast response.
    """
    return build_forecast(req)
