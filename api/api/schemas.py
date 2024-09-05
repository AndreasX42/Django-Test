from pydantic import BaseModel, Field, NonNegativeFloat, NonNegativeInt
from datetime import date


class PortfolioValuesForTimeT(BaseModel):
    t: date = Field(description="Timestep t in series")
    weights: dict[str, NonNegativeFloat] = Field(
        description="Asset mapped to its portfolio weight for time t."
    )
    portfolio_value: NonNegativeFloat = Field(
        description="Portfolio asset value for time t"
    )


class PortfolioValues(BaseModel):
    portfolio_id: NonNegativeInt = Field("The portfolio id")
    values: list[PortfolioValuesForTimeT] = Field(
        description="List of portfolio values between two dates"
    )


class CalculationResponseDto(BaseModel):
    portfolios: list[PortfolioValues] = Field(
        description="List of calculated portfolio values per portfolio"
    )
