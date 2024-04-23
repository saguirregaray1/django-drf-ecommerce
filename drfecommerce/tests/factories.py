import factory

from drfecommerce.product.models import (
    Product,
    Category,
    Brand,
    ProductImage,
    ProductLine,
    ProductType,
    Attribute,
    AttributeValue,
)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category_{n}")
    slug = factory.Sequence(lambda n: f"Category_{n}")
    is_active = True


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.Sequence(lambda n: f"Brand_{n}")
    is_active = True


class AttributeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Attribute

    name = factory.Sequence(lambda n: f"Attribute_{n}")
    description = factory.Sequence(lambda n: f"Description_{n}")


class AttributeValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AttributeValue

    attribute_value = factory.Sequence(lambda n: f"AttributeValue_{n}")
    attribute = factory.SubFactory(AttributeFactory)


class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductType
        skip_postgeneration_save = True

    name = factory.Sequence(lambda n: f"ProductType_{n}")

    @factory.post_generation
    def attribute(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.attribute.add(*extracted)
        self.save()


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f"Product_{n}")
    description = factory.Sequence(lambda n: f"Description_{n}")
    slug = factory.Sequence(lambda n: f"Product_{n}")
    is_digital = False
    brand = factory.SubFactory(BrandFactory)
    category = factory.SubFactory(CategoryFactory)
    is_active = True
    product_type = factory.SubFactory(ProductTypeFactory)


class ProductLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLine
        skip_postgeneration_save = True

    price = 10.0
    sku = factory.Sequence(lambda n: f"SKU_{n}")
    stock_qty = 5
    is_active = True
    product = factory.SubFactory(ProductFactory)
    order = factory.Sequence(lambda n: n)

    @factory.post_generation
    def attribute_value(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.attribute_value.add(*extracted)
        self.save()


class ProductImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductImage

    url = "test.jpg"
    alternative_text = "Test"
    productline = factory.SubFactory(ProductLineFactory)
    order = factory.Sequence(lambda n: n)
