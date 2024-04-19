import factory

from drfecommerce.product.models import (
    Product,
    Category,
    Brand,
    ProductImage,
    ProductLine,
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


class ProductLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLine

    price = 10.0
    sku = factory.Sequence(lambda n: f"SKU_{n}")
    stock_qty = 5
    is_active = True
    product = factory.SubFactory(ProductFactory)
    order = factory.Sequence(lambda n: n)


class ProductImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductImage

    url = "test.jpg"
    alternative_text = "Test"
    productline = factory.SubFactory(ProductLineFactory)
    order = factory.Sequence(lambda n: n)
