from django.db import models
from django.forms import ValidationError
from mptt.models import MPTTModel, TreeForeignKey
from .fields import OrderField


class ActiveQuerySet(models.QuerySet):
    def isactive(self):
        return self.filter(is_active=True)


class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
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

    product_type = models.ForeignKey(
        "ProductType", on_delete=models.PROTECT, related_name="product"
    )

    def __str__(self) -> str:
        return self.name


class Attribute(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name


class AttributeValue(models.Model):
    attribute_value = models.CharField(max_length=100)
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name="attribute_value"
    )

    def __str__(self) -> str:
        return f"{self.attribute.name}_{self.attribute_value}"


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

    attribute_value = models.ManyToManyField(
        AttributeValue,
        through="ProductLineAttributeValue",
        related_name="product_line_attribute_value",
    )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductLine, self).save(*args, **kwargs)

    def clean(self):
        qs = ProductLine.objects.filter(product=self.product_id)
        for obj in qs:
            if obj.id != self.id and obj.order == self.order:
                raise ValidationError("Duplicate value")

    def __str__(self) -> str:
        return f"product_line_{self.sku}"


class ProductLineAttributeValue(models.Model):
    productline = models.ForeignKey(
        ProductLine,
        on_delete=models.CASCADE,
        related_name="productline_attribute_value_pl",
    )
    attribute_value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
        related_name="productline_attribute_value_av",
    )

    class Meta:
        unique_together = ("productline", "attribute_value")

    def clean(self):
        qs = (
            ProductLineAttributeValue.objects.filter(productline=self.productline)
            .filter(attribute_value=self.attribute_value)
            .exists()
        )

        if not qs:
            iqs = Attribute.objects.filter(
                attribute_value__product_line_attribute_value=self.productline
            ).values_list("pk", flat=True)

            if self.attribute_value.attribute.id in list(iqs):
                raise ValidationError("Duplicate attribute value")


class ProductImage(models.Model):
    url = models.ImageField(upload_to=None, default="test.jpg")
    alternative_text = models.TextField()
    productline = models.ForeignKey(
        ProductLine, on_delete=models.CASCADE, related_name="product_image"
    )
    order = OrderField(unique_for_field="productline", blank=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductImage, self).save(*args, **kwargs)

    def clean(self):
        qs = ProductImage.objects.filter(productline=self.productline)
        for obj in qs:
            if obj.id != self.id and obj.order == self.order:
                raise ValidationError("Duplicate value")

    def __str__(self) -> str:
        return str(self.url)


class ProductType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    attribute = models.ManyToManyField(
        Attribute,
        through="ProductTypeAttribute",
        related_name="product_type_attribute",
    )

    def __str__(self) -> str:
        return str(self.name)


class ProductTypeAttribute(models.Model):
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,
        related_name="product_type_attribute_pt",
    )
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        related_name="product_type_attribute_a",
    )

    class Meta:
        unique_together = ("product_type", "attribute")
