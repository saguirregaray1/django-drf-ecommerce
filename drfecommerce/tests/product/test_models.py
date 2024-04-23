from django.forms import ValidationError
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


class TestProductTypeModel:
    def test_str_method(self, product_type_factory, attribute_factory):
        attr = attribute_factory(name="test_attr")
        obj = product_type_factory(name="test_type", attribute=(attr,))
        assert obj.__str__() == "test_type"


class TestProductModel:
    def test_str_method(self, product_factory, product_type_factory):
        obj = product_factory(name="test_product")
        assert obj.__str__() == "test_product"


class TestProductLineModel:
    def test_str_method(self, product_line_factory, attribute_value_factory):
        attr = attribute_value_factory(attribute_value="test_attr")
        obj = product_line_factory(sku="test_product", attribute_value=(attr,))
        assert obj.__str__() == f"product_line_{obj.sku}"

    def test_duplicate_order_values(self, product_factory, product_line_factory):
        product = product_factory()

        product_line_factory(order=1, product=product)

        with pytest.raises(ValidationError):
            product_line_factory(order=1, product=product).clean()


class TestProductImageModel:
    def test_str_method(self, product_image_factory):
        obj = product_image_factory()
        assert obj.__str__() == str(obj.url)
