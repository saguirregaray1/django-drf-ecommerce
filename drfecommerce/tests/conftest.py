from pytest_factoryboy import register
from rest_framework.test import APIClient
import pytest
from .factories import (
    CategoryFactory,
    ProductFactory,
    ProductImageFactory,
    ProductLineFactory,
    AttributeFactory,
    AttributeValueFactory,
    ProductTypeFactory,
    ProductLineAttributeValueFactory,
)

register(CategoryFactory)
register(ProductFactory)
register(ProductLineFactory)
register(ProductImageFactory)
register(AttributeFactory)
register(AttributeValueFactory)
register(ProductTypeFactory)
register(ProductLineAttributeValueFactory)


@pytest.fixture
def api_client():
    return APIClient
