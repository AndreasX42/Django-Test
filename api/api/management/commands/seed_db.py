import os
from typing import Any
import pandas as pd
from datetime import date

from django.conf import settings
from django.core.management.base import BaseCommand

from api.models import Asset, AssetInitials, AssetPrice

import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    INITIAL_PORTFOLIO_VALUE = 1_000_000_000

    # cache asset objects
    assets_map = {}

    def handle(self, *args: Any, **options: Any) -> str | None:

        logger.info("Starting to seed db...")

        excel_file_path = os.path.join(settings.BASE_DIR, "resources", "datos.xlsx")

        datos = pd.ExcelFile(excel_file_path)
        weights_df = pd.read_excel(datos, "weights")
        prices_df = pd.read_excel(datos, "Precios")

        # reset db
        Asset.objects.all().delete()
        AssetInitials.objects.all().delete()
        AssetPrice.objects.all().delete()

        # initialize Asset table
        self.initialize_assets(weights_df.activos.values)

        # initialize initial asset values
        self.initialize_asset_initials(weights_df, prices_df)

        # initialize asset prices
        self.initialize_asset_prices(prices_df)

        logger.info("Completed seeding db...")

    def initialize_assets(self, asset_names: list[str]):
        for asset_name in asset_names:
            asset = Asset.objects.create(asset_name=asset_name)
            self.assets_map[asset_name] = asset

    def initialize_asset_initials(
        self, weights_df: pd.DataFrame, prices_df: pd.DataFrame
    ):

        # calculate initial quantity for all assets and portfolios
        initial_prices = prices_df.iloc[0].values[1:]
        initial_weights_p1 = weights_df["portafolio 1"].values
        initial_weights_p2 = weights_df["portafolio 2"].values

        initial_quantities_p1 = (
            initial_weights_p1 * self.INITIAL_PORTFOLIO_VALUE
        ) / initial_prices

        initial_quantities_p2 = (
            initial_weights_p2 * self.INITIAL_PORTFOLIO_VALUE
        ) / initial_prices

        for i, (fecha, asset_name, weight_p1, weight_p2) in weights_df.iterrows():

            # create asset entity for portfolio 1
            self.create_asset_initials(
                asset_name=self.assets_map[asset_name],
                portfolio_id=1,
                initial_weight=weight_p1,
                initial_quantity=initial_quantities_p1[i],
            )

            # create asset entity for portfolio 2
            self.create_asset_initials(
                asset_name=self.assets_map[asset_name],
                portfolio_id=2,
                initial_weight=weight_p2,
                initial_quantity=initial_quantities_p2[i],
            )

    def initialize_asset_prices(self, prices_df: pd.DataFrame):

        # convert datetime objects into dates
        dates_list = [pd.to_datetime(d).date() for d in prices_df.Dates.values]

        for asset_name, price_data in prices_df.iloc[:, 1:].items():

            for price_date, price in zip(dates_list, price_data):
                AssetPrice.objects.create(
                    asset_name=self.assets_map[asset_name], date=price_date, price=price
                )

    def create_asset_initials(
        self,
        asset_name: Asset,
        portfolio_id: int,
        initial_weight: float,
        initial_quantity: float,
    ):

        # create table row for portfolio weight data
        AssetInitials.objects.create(
            asset_name=asset_name,
            portfolio_id=portfolio_id,
            initial_weight=initial_weight,
            initial_quantity=initial_quantity,
        )

    def create_asset_price(self, price_data: date, asset_name: str, price: float):
        # create table row for portfolio price data
        AssetPrice.objects.create(
            asset_name=asset_name,
            date=price_data,
            price=price,
        )
