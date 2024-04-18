import factory

from drfecommerce.product.models import Product, Category, Brand


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category_{n}")
    is_active = True


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.Sequence(lambda n: f"Brand_{n}")
    is_active = True


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f"Product_1{n}")
    description = factory.Sequence(lambda n: f"Description_{n}")
    slug = factory.Sequence(lambda n: f"Product_1{n}")
    is_digital = False
    brand = factory.SubFactory(BrandFactory)
    category = factory.SubFactory(CategoryFactory)
    is_active = True
