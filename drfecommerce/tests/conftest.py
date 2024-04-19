from pytest_factoryboy import register
from rest_framework.test import APIClient
import pytest
from .factories import (
    BrandFactory,
    CategoryFactory,
    ProductFactory,
    ProductImageFactory,
    ProductLineFactory,
)

register(CategoryFactory)
register(BrandFactory)
register(ProductFactory)
register(ProductLineFactory)
register(ProductImageFactory)


@pytest.fixture
def api_client():
    return APIClient
