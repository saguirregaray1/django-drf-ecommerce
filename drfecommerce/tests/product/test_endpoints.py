import pytest
import json

pytestmark = pytest.mark.django_db


class TestCategoryEndpoints:
    endpoint = "/api/category/"

    def test_list_categories(self, category_factory, api_client):
        # Arrange
        category_factory.create_batch(10)
        # Act
        response = api_client().get(self.endpoint)
        # Assert
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 10


class TestBrandEndpoints:
    endpoint = "/api/brand/"

    def test_list_categories(self, brand_factory, api_client):

        brand_factory.create_batch(10)

        response = api_client().get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 10


class TestProductEndpoints:
    endpoint = "/api/product/"

    def test_list_categories(self, product_factory, api_client):

        product_factory.create_batch(10)

        response = api_client().get(self.endpoint)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 10
