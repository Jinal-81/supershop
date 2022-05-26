from rest_framework import filters
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from product.models import Product, Category
from product.serializer import ProductSerializer, CategorySerializer, ProductSerializerV1
from product.views import product_info_logger, product_warning_logger

PRODUCT_V2_LOG_MSG = "product serializer v2 called with name field only."
PRODUCT_V1_LOG_MSG = "product serializer v1 called with all the fields."
PAGE_SIZE_NONE_LOG_MSG = "return product by page size!!"
PAGE_SIZE_LOG_MSG = "get all the pages successfully"
CATEGORY_SELECTED_LOG_MSG = 'category selected successfully'
PRODUCT_SEARCH_LOG_MSG = 'search product by their name'


class CustomNumberPagination(PageNumberPagination):
    """api for the pagination."""
    pagination_class = PageNumberPagination  # pagination class
    page_size_query_param = 'size'  # items per page

    def get_page_size(self, request):
        """get page size parameter."""
        # import pdb; pdb.set_trace()
        size_page = request.GET.get('size')  # get page size

        if size_page and size_page.upper() == 'ALL':  # check that page size is all or any number or none
            # queryset_count = Product.objects.count()  # if all then return total record count.
            product_info_logger.info(PAGE_SIZE_LOG_MSG)
            return None  # return None (see the super method of the model view set)
        else:
            product_warning_logger.warning(PAGE_SIZE_NONE_LOG_MSG)
            return super(CustomNumberPagination, self).get_page_size(request)  # else call super and return that size.


class ProductApi(viewsets.ModelViewSet):
    """API for the product using modelViewSet for view and edit products."""
    queryset = Product.objects.all()  # fetch all the products.
    pagination_class = CustomNumberPagination  # call pagination for the products.
    serializer_class = ProductSerializer  # call serializer for the products.

    ordering = ['id']  # ordering according id.
    filter_backends = (filters.SearchFilter,)  # set search filter.
    search_fields = ('name',)  # search according product's name.
    product_info_logger.info(PRODUCT_SEARCH_LOG_MSG)
    permission_classes = [IsAuthenticated]  # user need to log in into system to access this api

    def get_serializer_class(self):
        """get version and called serializer according version."""
        # import pdb; pdb.set_trace()
        if self.request.version == 'v5':  # check version
            product_info_logger.info(PRODUCT_V2_LOG_MSG)
            return ProductSerializerV1  # call serializer according version.
        product_info_logger.info(PRODUCT_V1_LOG_MSG)
        return ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """API for the category using modelViewSet and router."""
    product_info_logger.info(CATEGORY_SELECTED_LOG_MSG)
    queryset = Category.objects.all()  # fetch all the categories.
    serializer_class = CategorySerializer  # set serializer class.
    permission_classes = [IsAuthenticated]  # user need to log in into system to access this api.



