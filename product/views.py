import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect

from cart.models import Cart, CartItem
from product.filters import ProductFilter
from product.models import Product

# Create your views here.
VIEW_PRODUCT_URL = "product/productdetail.html"
PRODUCT_NOT_AVAILABLE_ERROR_MSG = 'Product is not available, Maybe you entered More quantity then available'
CART_UPDATE_MSG = "Cart updated!"
VIEW_ALL_PRODUCT_URL = "product/productlist.html"
VIEW_PRODUCT_LOG_MSG = 'View Particular product successfully.'
PRODUCT_PAGE_LOAD_LOG_MSG = "Product list page load successfully"
PAGE_IS_NOT_INTEGER_LOG_MSG = "page is not an integer."
PAGE_EMPTY_LOG_MSG = "page is empty."
CART_CREATE_LOG_MSG = "cart create successfully."

product_info_logger = logging.getLogger('product_info')
product_info_logger.info('log into product app.')

product_warning_logger = logging.getLogger('product_warning')
product_warning_logger.info('log into product app.')

product_debug_logger = logging.getLogger('product_debug')
product_debug_logger.info('log into product app.')


def custom_get_or_create(user, status):
    """
    create or get the object.
    """
    get_object, create_object = Cart.objects.get_or_create(user=user, status=status)
    product_info_logger.info(CART_CREATE_LOG_MSG)
    return get_object, create_object


@login_required
def view_product(request, id):
    """
    view available product details.
    """
    if request.method == "POST":
        product = get_object_or_404(Product, id=id)  # if modal and object is not exists then rains 404 error.
        cart, created = custom_get_or_create(request.user, Cart.StatusInCart.OPEN)  # return tuple (cart,created)
        cart.save()  # save data into cart
        cartquantity = request.POST.get('quantity')
        if int(cartquantity) > product.quantity:  # if user enter quantity more than available product quantity.
            product_warning_logger.warning(PRODUCT_NOT_AVAILABLE_ERROR_MSG)
            messages.error(request, PRODUCT_NOT_AVAILABLE_ERROR_MSG)
            return redirect('cart')
        else:
            cartitem, created = CartItem.objects.get_or_create(product=product, cart=cart)  # create or get the object and
            # return the tuple (cartitem,created)
            cartitem.quantity = request.POST.get('quantity')
            cartitem.price = product.price
            cartitem.save()  # save the data into cartitem
            product_info_logger.info(CART_UPDATE_MSG)
            messages.success(request, CART_UPDATE_MSG)
            return redirect('cart')

    product = Product.objects.get(id=id)  # view the particular product
    product_debug_logger.debug(VIEW_PRODUCT_LOG_MSG)
    return render(request, VIEW_PRODUCT_URL, {'product': product})


def product_list(request):
    """
    product list out page.
    """
    products = Product.objects.all().order_by('id')  # fetch all the products
    user_filter = ProductFilter(request.POST, queryset=products)  # filter product by their name
    products = user_filter.qs  # filtered result
    page = request.GET.get('page', 1)  # get the page

    paginator = Paginator(products, 9)  # tell the paginator to paginate products queryset in 9 products per page
    try:
        products_item = paginator.page(page)
    except PageNotAnInteger:
        products_item = paginator.page(1)  # if page is not integer
        product_warning_logger.warning(PAGE_IS_NOT_INTEGER_LOG_MSG)
    except EmptyPage:
        products_item = paginator.page(paginator.num_pages)  # if page is empty.
        product_warning_logger.warning(PAGE_EMPTY_LOG_MSG)
    product_info_logger.info(PRODUCT_PAGE_LOAD_LOG_MSG)
    return render(request, VIEW_ALL_PRODUCT_URL, {'filter': user_filter, 'products_item': products_item})