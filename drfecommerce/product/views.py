from rest_framework import viewsets
from rest_framework.response import Response
from .models import Category, Brand, Product
from .serializers import CategorySerializer, BrandSerializer, ProductSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from django.db.models import Prefetch


class CategoryViewSet(viewsets.ViewSet):

    queryset = Category.objects.all().isactive()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        """
        Endpoint to retrieve all categories
        """
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)


class BrandViewSet(viewsets.ViewSet):

    queryset = Brand.objects.all().isactive()

    @extend_schema(responses=BrandSerializer)
    def list(self, request):
        """
        Endpoint to retrieve all brands
        """
        serializer = BrandSerializer(self.queryset, many=True)

        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet):

    queryset = Product.objects.all().isactive()
    lookup_field = "slug"

    def retrieve(self, request, slug=None):
        """
        Endpoint to retrieve a single product
        """
        serializer = ProductSerializer(
            self.queryset.filter(slug=slug)
            .select_related("category", "brand")
            .prefetch_related(Prefetch("product_line__product_image"))
            .prefetch_related(Prefetch("product_line__attribute_value__attribute")),
            many=True,
        )

        return Response(serializer.data)

    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        """
        Endpoint to retrieve all products
        """
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        url_path=r"category/(?P<slug>\w+)/all",
    )
    def list_product_by_slug(self, request, slug=None):
        """
        Endpoint to retrieve products by category
        """
        serializer = ProductSerializer(
            self.queryset.filter(category__slug=slug), many=True
        )
        return Response(serializer.data)
