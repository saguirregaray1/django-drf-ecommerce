from django.db import models
from django.forms import ValidationError
from mptt.models import MPTTModel, TreeForeignKey
from .fields import OrderField


class IsActiveQuerySet(models.QuerySet):
    def is_active(self):
        return self.filter(is_active=True)


class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)
    objects = IsActiveQuerySet.as_manager()

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True)
    pid = models.CharField(max_length=10, unique=True)
    description = models.TextField()
    is_digital = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    category = TreeForeignKey("Category", on_delete=models.PROTECT)
    product_type = models.ForeignKey(
        "ProductType", on_delete=models.PROTECT, related_name="product"
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    attribute_value = models.ManyToManyField(
        "AttributeValue",
        through="ProductAttributeValue",
        related_name="product_attribute_value",
    )

    objects = IsActiveQuerySet.as_manager()

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
        Product, on_delete=models.PROTECT, related_name="product_line"
    )
    product_type = models.ForeignKey(
        "ProductType", on_delete=models.PROTECT, related_name="product_line_type"
    )
    order = OrderField(unique_for_field="product", blank=True)
    weight = models.FloatField()

    attribute_value = models.ManyToManyField(
        AttributeValue,
        through="ProductLineAttributeValue",
        related_name="product_line_attribute_value",
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    objects = IsActiveQuerySet.as_manager()

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
    product_line = models.ForeignKey(
        ProductLine,
        on_delete=models.CASCADE,
        related_name="product_line_attribute_value_pl",
    )
    attribute_value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
        related_name="product_line_attribute_value_av",
    )

    class Meta:
        unique_together = ("product_line", "attribute_value")

    def clean(self):
        print(self.product_line)
        print(self.attribute_value)
        qs = ProductLineAttributeValue.objects.filter(
            attribute_value=self.attribute_value
        ).filter(product_line=self.product_line)

        if not qs:
            iqs = Attribute.objects.filter(
                attribute_value__product_line_attribute_value=self.product_line
            ).values_list("pk", flat=True)

            if self.attribute_value.attribute.id in list(iqs):
                raise ValidationError("Duplicate attribute value")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductLineAttributeValue, self).save(*args, **kwargs)


class ProductAttributeValue(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_attribute_value_p",
    )
    attribute_value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
        related_name="product_attribute_value_av",
    )

    class Meta:
        unique_together = ("product", "attribute_value")


class ProductImage(models.Model):
    url = models.ImageField(upload_to=None, default="test.jpg")
    alternative_text = models.TextField()
    product_line = models.ForeignKey(
        ProductLine, on_delete=models.CASCADE, related_name="product_image"
    )
    order = OrderField(unique_for_field="product_line", blank=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductImage, self).save(*args, **kwargs)

    def clean(self):
        qs = ProductImage.objects.filter(product_line=self.product_line)
        for obj in qs:
            if obj.id != self.id and obj.order == self.order:
                raise ValidationError("Duplicate value")

    def __str__(self) -> str:
        return f"{self.product_line.sku}_img"


class ProductType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)
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
