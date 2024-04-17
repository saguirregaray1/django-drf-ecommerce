import pytest

pytestmark = pytest.mark.django_db


class TestCategoryModel:
    def test_str_method(self, category_factory):
        # Arrange
        # Act
        obj = category_factory(name="test_cat")
        # Assert
        assert obj.__str__() == "test_cat"


class TestBrandModel:
    def test_str_method(self, brand_factory):
        obj = brand_factory(name="test_brand")
        assert obj.__str__() == "test_brand"


class TestProductModel:
    def test_str_method(self, product_factory):
        obj = product_factory(name="test_product")
        assert obj.__str__() == "test_product"
