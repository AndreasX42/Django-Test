from django.db import models


class Asset(models.Model):
    # id = models.PositiveIntegerField(primary_key=True, editable=False, null=False)
    asset_name = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        db_table = "assets"
        constraints = [
            models.UniqueConstraint(
                fields=["asset_name"],
                name="unique_asset_name",
            )
        ]

    def __str__(self):
        return f"Asset[name={self.asset_name}]"


class AssetInitials(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    portfolio_id = models.PositiveIntegerField(null=False)
    initial_quantity = models.DecimalField(max_digits=32, decimal_places=8, null=False)
    initial_weight = models.DecimalField(max_digits=6, decimal_places=4, null=False)

    class Meta:
        db_table = "asset_initials"
        constraints = [
            models.UniqueConstraint(
                fields=["asset", "portfolio_id"],
                name="unique_asset_portfolio_id",
            )
        ]

    def __str__(self):
        return f"AssetInitials[name={self.asset.asset_name}, portfolio_id={self.portfolio_id}, c_0={self.initial_quantity}, w_0={self.initial_weight}]"


class AssetPrice(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    date = models.DateField(null=False)
    price = models.DecimalField(max_digits=32, decimal_places=8, null=False)

    class Meta:
        db_table = "asset_prices"
        constraints = [
            models.UniqueConstraint(fields=["asset", "date"], name="unique_asset_date")
        ]

    def __str__(self):
        return f"AssetPrice[asset={self.asset.asset_name}, date={self.date}, price={self.price}]"
