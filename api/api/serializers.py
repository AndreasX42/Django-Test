# serializers.py
from rest_framework import serializers
from api.models import Asset, AssetInitials, AssetPrice


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ["id", "asset_name"]


class AssetInitialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetInitials
        fields = [
            "id",
            "asset_name",
            "portfolio_id",
            "initial_quantity",
            "initial_weight",
        ]


class AssetPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetPrice
        fields = ["id", "asset_name", "date", "price"]
