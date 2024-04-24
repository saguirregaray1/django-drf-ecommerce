from django.db import IntegrityError
from django.forms import ValidationError
import pytest

from ...product.models import Product, ProductLine

pytestmark = pytest.mark.django_db


class TestCategoryModel:
    def test_str_method(self, category_factory):
        # Arrange
        # Act
        obj = category_factory(name="test_cat")
        # Assert
        assert obj.__str__() == "test_cat"

    def test_name_max_length(self, category_factory):
        obj = category_factory(name="a" * 101)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_slug_max_length(self, category_factory):
        obj = category_factory(slug="a" * 256)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_name_unique_field(self, category_factory):
        category_factory(name="test")
        with pytest.raises(IntegrityError):
            category_factory(name="test").full_clean()

    def test_slug_unique_field(self, category_factory):
        category_factory(slug="test")
        with pytest.raises(IntegrityError):
            category_factory(slug="test").full_clean()


class TestProductTypeModel:
    def test_str_method(self, product_type_factory, attribute_factory):
        attr = attribute_factory(name="test_attr")
        obj = product_type_factory(name="test_type", attribute=(attr,))
        assert obj.__str__() == "test_type"

    def test_name_max_length(self, product_type_factory):
        obj = product_type_factory(name="a" * 101)
        with pytest.raises(ValidationError):
            obj.full_clean()


class TestProductModel:
    def test_str_method(self, product_factory):
        obj = product_factory(name="test_product")
        assert obj.__str__() == "test_product"

    def test_name_max_length(self, product_factory):
        obj = product_factory(name="a" * 101)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_slug_max_length(self, product_factory):
        obj = product_factory(slug="a" * 256)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_pid_max_length(self, product_factory):
        obj = product_factory(pid="a" * 11)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_is_digital_false(self, product_factory):
        obj = product_factory()
        assert obj.is_digital is False

    def test_fk_category_on_delete_protect(self, category_factory, product_factory):
        obj = category_factory()
        product_factory(category=obj)
        with pytest.raises(IntegrityError):
            obj.delete()

    def test_return_product_active_only_true(self, product_factory):
        product_factory(is_active=False)
        product_factory(is_active=True)
        qs = Product.objects.is_active().count()
        assert qs == 1

    def test_return_product_active_only_false(self, product_factory):
        product_factory(is_active=False)
        product_factory(is_active=True)
        qs = Product.objects.count()
        assert qs == 2


class TestProductLineModel:

    def test_duplicate_attribute_inserts(
        self,
        product_line_factory,
        attribute_value_factory,
        attribute_factory,
        product_line_attribute_value_factory,
    ):
        attr = attribute_factory(name="shoe-color")
        attr_value_1 = attribute_value_factory(attribute=attr, attribute_value="red")
        attr_value_2 = attribute_value_factory(attribute=attr, attribute_value="blue")
        product_line = product_line_factory()
        product_line_attribute_value_factory(
            product_line=product_line, attribute_value=attr_value_1
        )
        with pytest.raises(ValidationError):
            product_line_attribute_value_factory(
                product_line=product_line, attribute_value=attr_value_2
            )

    def test_str_method(self, product_line_factory, attribute_value_factory):
        attr = attribute_value_factory(attribute_value="test_attr")
        obj = product_line_factory(sku="test_product", attribute_value=(attr,))
        assert obj.__str__() == f"product_line_{obj.sku}"

    def test_duplicate_order_values(self, product_factory, product_line_factory):
        product = product_factory()

        product_line_factory(order=1, product=product)

        with pytest.raises(ValidationError):
            product_line_factory(order=1, product=product).clean()

    def test_field_decimal_places(self, product_line_factory):
        price = 1.001
        with pytest.raises(ValidationError):
            product_line_factory(price=price)

    def test_field_price_max_digits(self, product_line_factory):
        price = 10000000000
        with pytest.raises(ValidationError):
            product_line_factory(price=price)

    def test_field_sku_max_length(self, product_line_factory):
        sku = "a" * 101
        with pytest.raises(ValidationError):
            product_line_factory(sku=sku)

    def test_is_active_false_default(self, product_line_factory):
        obj = product_line_factory(is_active=False)
        assert obj.is_active is False

    def test_fk_product_on_delete_protect(self, product_factory, product_line_factory):
        obj1 = product_factory()
        product_line_factory(product=obj1)
        with pytest.raises(IntegrityError):
            obj1.delete()

    def test_fk_product_type_on_delete_protect(
        self, product_type_factory, product_line_factory
    ):
        obj1 = product_type_factory()
        product_line_factory(product_type=obj1)
        with pytest.raises(IntegrityError):
            obj1.delete()

    def test_return_product_active_onyl_true(self, product_line_factory):
        product_line_factory(is_active=False)
        product_line_factory(is_active=True)
        qs = ProductLine.objects.is_active().count()
        assert qs == 1

    def test_return_product_active_only_false(self, product_line_factory):
        product_line_factory(is_active=False)
        product_line_factory(is_active=True)
        qs = ProductLine.objects.count()
        assert qs == 2


class TestProductImageModel:
    def test_str_method(self, product_image_factory, product_line_factory):
        obj1 = product_line_factory(sku="11")
        obj = product_image_factory(product_line=obj1)
        assert obj.__str__() == f"{obj1.sku}_img"

    def test_duplicate_order_values(self, product_image_factory, product_line_factory):
        obj = product_line_factory()

        product_image_factory(order=1, product_line=obj)

        with pytest.raises(ValidationError):
            product_image_factory(order=1, product_line=obj).clean()


class TestAttributeModel:
    def test_str_method(self, attribute_factory):
        obj = attribute_factory(name="test_attr")
        assert obj.__str__() == "test_attr"

    def test_name_field_max_length(self, attribute_factory):
        obj = attribute_factory(name="a" * 101)
        with pytest.raises(ValidationError):
            obj.full_clean()


class TestAttributeValueModel:
    def test_str_method(self, attribute_value_factory, attribute_factory):
        obj1 = attribute_factory(name="test_attr")
        obj2 = attribute_value_factory(attribute=obj1, attribute_value="test_value")
        assert obj2.__str__() == "test_attr_test_value"

    def test_attribute_value_max_length(self, attribute_value_factory):
        obj2 = attribute_value_factory(attribute_value="a" * 101)
        with pytest.raises(ValidationError):
            obj2.full_clean()
