import pytest
import json

pytestmark = pytest.mark.django_db


class TestCategoryEndpoints:
    endpoint = "/api/category/"

    def test_list_all(self, category_factory, api_client):
        # Arrange
        category_factory.create_batch(10)
        # Act
        response = api_client().get(self.endpoint)
        # Assert
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 10


class TestProductEndpoints:
    endpoint = "/api/product/"

    def test_list_all(self, product_factory, api_client):

        product_factory.create_batch(10)

        response = api_client().get(self.endpoint)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 10

    def test_get_one_by_slug(self, product_factory, api_client):
        obj = product_factory(slug="test")

        response = api_client().get(f"{self.endpoint}{obj.slug}/")
        assert response.status_code == 200
        assert json.loads(response.content)[0]["slug"] == "test"

    def test_get_by_category_slug(self, product_factory, category_factory, api_client):
        cat_1 = category_factory(slug="cat1")
        cat_2 = category_factory(slug="cat2")
        product_factory(category=cat_1)
        product_factory(category=cat_2)

        response = api_client().get(f"{self.endpoint}category/{cat_1.slug}/all/")
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1
