from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from product.models import Product
from cart.models import Cart, CartItem
# Create your views here.
VIEW_PRODUCT_URL = "product/productdetail.html"
PRODUCT_NOT_AVAILABLE_ERROR_MSG = 'Product is not available, Maybe you entered More quantity then available'
CART_UPDATE_MSG = "Cart updated!"


def custom_get_or_create(user, status):
    """
    create or get the object.
    """
    get_object, create_object = Cart.objects.get_or_create(user=user, status=status)
    return get_object, create_object


@login_required
def view_product(request, id):
    """
    view available product details.
    """
    if request.method == "POST":
        product = get_object_or_404(Product, id=id)  # if modal and object is not exists then rains 404 error.
        cart, created = custom_get_or_create(request.user, "open")  # return tuple (cart,created)
        cart.save()  # save data into cart
        cartquantity = request.POST.get('quantity')
        if int(cartquantity) > product.quantity:  # if user enter quantity more than available product quantity.
            messages.error(request, PRODUCT_NOT_AVAILABLE_ERROR_MSG)
            return redirect('cart')
        else:
            cartitem, created = CartItem.objects.get_or_create(product=product, cart=cart)  # create or get the object and
            # return the tuple (cartitem,created)
            cartitem.quantity = request.POST.get('quantity')
            cartitem.price = product.price
            cartitem.save()  # save the data into cartitem
            messages.success(request, CART_UPDATE_MSG)
            return redirect('cart')

    product = Product.objects.get(id=id)  # view the particular product
    return render(request, VIEW_PRODUCT_URL, {'product': product})