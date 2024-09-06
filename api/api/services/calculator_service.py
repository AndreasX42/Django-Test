from datetime import datetime, timedelta
import numpy as np

from api.models import Asset, AssetInitials, AssetPrice
from api.schemas import (
    PortfolioValues,
    PortfolioValuesForTimeT,
    CalculationResponseDto,
)

import logging

logger = logging.getLogger(__name__)


def calculate_portfolio_values(
    start_date: datetime, end_date: datetime
) -> CalculationResponseDto:
    """Main method for calculation of portfolio values

    Args:
        start_date (datetime): Calculation start date
        end_date (datetime): Calculation end date

    Returns:
        CalculationResponseDto: Response dto with all calculated values
    """

    logger.info("Starting calculation for range {%s}-{%s}", start_date, end_date)

    # calculate all values between given dates for portfolio 1
    portfolio_values_for_p1 = calculate_values_for_portfolio(
        portfolio_id=1, start_date=start_date, end_date=end_date
    )

    # calculate all values between given dates for portfolio 2
    portfolio_values_for_p2 = calculate_values_for_portfolio(
        portfolio_id=2, start_date=start_date, end_date=end_date
    )

    # return result in pydantic dto
    return CalculationResponseDto(
        portfolios=[portfolio_values_for_p1, portfolio_values_for_p2]
    )


def calculate_values_for_portfolio(
    portfolio_id: int, start_date: datetime, end_date: datetime
) -> PortfolioValues:
    """Calculates asset weights and portfolio market value for each day between given dates

    Args:
        portfolio_id (int): Id of portfolio
        start_date (datetime): Start date of calculation
        end_date (datetime): End date of calculation

    Returns:
        PortfolioValues: Calculation result
    """

    portfolio_values = []
    current_date = start_date

    while current_date <= end_date:
        result = calculate_values_at_t_for_portfolio(
            portfolio_id=portfolio_id, date=current_date
        )
        portfolio_values.append(result)
        current_date += timedelta(days=1)

    return PortfolioValues(portfolio_id=portfolio_id, values=portfolio_values)


def calculate_values_at_t_for_portfolio(
    portfolio_id: int, date: datetime
) -> PortfolioValuesForTimeT:
    """Calculates asset weights and portfolio market value for given date

    Args:
        portfolio_id (int): Id of portfolio
        date (datetime): Calculation date

    Returns:
        PortfolioValuesForTimeT: Calculation result
    """

    assets = Asset.objects.all()

    # get the prices for each asset for the specific date
    price_data = AssetPrice.objects.filter(date=date)

    # order prices according to order of asset names in assets list
    prices_map = {data.asset: float(data.price) for data in price_data}
    asset_prices = np.array([prices_map.get(asset, 0.0) for asset in assets])

    # get the quantity per asset from initial values
    asset_quantities = np.array([0] * len(assets))
    for i, asset in enumerate(assets):
        initials = AssetInitials.objects.get(portfolio_id=portfolio_id, asset=asset)
        asset_quantities[i] = initials.initial_quantity

    # both numpy arrays are sorted correctly according to assets
    # calculate the current market value for each asset
    asset_values = asset_quantities * asset_prices

    # round values to 2 decimals
    asset_values = np.round(asset_values, 2, out=asset_values)

    # sum of asset values is V_t
    v_t = np.round(np.sum(asset_values), 2)

    # asset weights are the market values divided by the overall market value
    asset_weights = asset_values / v_t

    # round asset weights to 4 decimals
    asset_weights = np.round(asset_weights, 4, out=asset_weights)

    # create PortfolioValuesForTimeT object from pydantic schema
    asset_names = [asset.asset_name for asset in assets]
    weights_dict = dict(zip(asset_names, asset_weights))

    return PortfolioValuesForTimeT(t=date, weights=weights_dict, portfolio_value=v_t)
