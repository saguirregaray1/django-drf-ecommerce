from django.db import models
from django.forms import ValidationError
from mptt.models import MPTTModel, TreeForeignKey
from .fields import OrderField


class ActiveQuerySet(models.QuerySet):
    def isactive(self):
        return self.filter(is_active=True)


class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    objects = ActiveQuerySet.as_manager()

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self) -> str:
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=False)
    objects = ActiveQuerySet.as_manager()

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    is_digital = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    category = TreeForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, blank=True
    )

    objects = ActiveQuerySet.as_manager()

    def __str__(self) -> str:
        return self.name


class ProductLine(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=100, unique=True)
    stock_qty = models.IntegerField()
    is_active = models.BooleanField(default=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_line"
    )
    order = OrderField(unique_for_field="product", blank=True)
    objects = ActiveQuerySet.as_manager()

    def clean_fields(self, exclude):
        super().clean_fields(exclude)
        qs = ProductLine.objects.filter(product=self.product)
        for obj in qs:
            if obj.id != self.id and (obj.order == self.order or obj.sku == self.sku):
                raise ValidationError("Duplicate value")

    def __str__(self) -> str:
        return f"product_line_{self.sku}"
