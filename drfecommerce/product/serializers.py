from rest_framework import serializers

from .models import (
    AttributeValue,
    Attribute,
    Category,
    Product,
    ProductImage,
    ProductLine,
)


class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="name")

    class Meta:
        model = Category
        fields = ["category_name"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ["id", "product_line"]


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ["id", "name"]


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(many=False)

    class Meta:
        model = AttributeValue
        fields = ["attribute_value", "attribute"]


class ProductLineSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)
    attribute_value = AttributeValueSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = [
            "price",
            "sku",
            "stock_qty",
            "is_active",
            "product_image",
            "attribute_value",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        av_data = data.pop("attribute_value")
        attr_values = {av["attribute"]["id"]: av["attribute_value"] for av in av_data}
        data.update({"specification": attr_values})
        return data


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name")
    product_line = ProductLineSerializer(many=True)
    attributes = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "name",
            "slug",
            "description",
            "is_digital",
            "is_active",
            "category_name",
            "product_line",
            "attributes",
        ]

    def get_attributes(self, obj):
        attributes = Attribute.objects.filter(
            product_type_attribute__product__id=obj.id
        )

        return AttributeSerializer(attributes, many=True).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        av_data = data.pop("attributes")
        attr = {av["id"]: av["name"] for av in av_data}
        data.update({"type specification": attr})
        return data
