from datetime import datetime

from pydantic import ValidationError
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Asset
from .serializers import AssetSerializer
from .services.calculator_service import calculate_portfolio_values


@api_view(["GET"])
def get_asset_names(request):

    assets = Asset.objects.all()
    serializer = AssetSerializer(assets, many=True)

    return Response(serializer.data, status.HTTP_200_OK)


@api_view(["GET"])
def get_portfolio_values(request):

    try:
        # inputs are two query params for start and end dates
        start_date = request.query_params.get("fecha_inicio")
        end_date = request.query_params.get("fecha_fin")
        # do some validations
        if not start_date or not end_date:
            return Response(
                {"error": "Ambos fechas para inicio y fin son requeridos."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"error": "Formato no válido, se espera formato 'YYYY-MM-DD'."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # calculate values for given dates
        result = calculate_portfolio_values(start_date, end_date)

        return JsonResponse(result.model_dump(), status=status.HTTP_200_OK)

    except ValidationError as e:
        return JsonResponse(
            {"error message": e.errors()}, status=status.HTTP_400_BAD_REQUEST
        )
