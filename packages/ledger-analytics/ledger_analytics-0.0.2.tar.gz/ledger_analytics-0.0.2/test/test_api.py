import pytest
from bermuda import meyers_tri
from bermuda import Triangle as BermudaTriangle
import requests

from ledger_analytics import AnalyticsClient, Triangle, DevelopmentModel, TailModel, ForecastModel


def test_ledger_analytics_creation():
    assert isinstance(AnalyticsClient(), AnalyticsClient)

    client = AnalyticsClient()
    assert client.host == "http://localhost:8000/analytics/"


def test_ledger_analytics_models():
    client = AnalyticsClient()
    assert isinstance(client.triangle, Triangle)
    assert isinstance(client.development_model, DevelopmentModel)
    assert isinstance(client.tail_model, TailModel)
    assert isinstance(client.forecast_model, ForecastModel)

def test_ledger_analytics_triangle_crud():
    client = AnalyticsClient()
    triangles = client.triangle.list()
    breakpoint()
    triangle_fixture = client.triangle.get(triangle_id="triangle2tdg16hT6LRBROt9EOjbFxxAkMH")
    triangle_create = client.triangle.create(
        config={
            "triangle_name": "test_meyers_triangle",
            "triangle_data": meyers_tri.to_dict(),
        }
    )
    assert triangle_create.post_response.status_code == 201
    triangle_get = client.triangle.get(triangle_id=triangle_create.triangle_id)
    assert triangle_create.triangle_id is not None
    assert isinstance(triangle_get, BermudaTriangle)

    client.triangle.delete(triangle_id=triangle_create.triangle_id)

    with pytest.raises(requests.HTTPError):
        client.triangle.get(triangle_id=triangle_create.triangle_id)
