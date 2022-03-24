from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from cart.models import Cart, CartItem
# Create your views here.

CART_URL = "cart/carttry.html"
ORDER_URL = 'cart/order.html'
CARTITEM_DELETE_MSG = "Cartitem deleted!"
CARTITEM_UPDATED_MSG = "quantity updated!"
CARTITEM_PLACED_MSG = "Cart placed!"


@login_required(login_url='/login/')
def cart(request):
    """
    redirect to cart page
    """
    user_cart = Cart.objects.filter(user=request.user, status="open").first()  # filter current user's cart
    return render(request, CART_URL, {'cart': user_cart})


@login_required(login_url='/login/')
def cart_item_remove(request, id):
    """
    remove item from the cart items.
    """
    cartitem = CartItem.objects.get(id=id)  # get cartitem
    cartitem.cart.total_amount = cartitem.cart.total_amount - (cartitem.price * cartitem.quantity)  # update
    # total_amount using cartitem price and quantity
    cartitem.cart.save()  # save updated total price
    cartitem.delete()  # delete cartitem
    messages.error(request, CARTITEM_DELETE_MSG)
    return redirect('cart')


@login_required(login_url='/login/')
def cart_item_update(request, id):
    """
    update item quantity and update total price accordingly.
    """
    cartitem = CartItem.objects.get(id=id)  # get cartitem
    cartitem.quantity = request.POST.get('quantity')  # get quantity from the user
    cartitem.cart.total_amount = cartitem.cart.total_amount + (int(cartitem.price) * int(cartitem.quantity))  # update
    # total price of the cart according cartitem price and cartitem quantity
    cartitem.save()
    messages.success(request, CARTITEM_UPDATED_MSG)
    return redirect('cart')


@login_required(login_url='/login/')
def order(request):
    """
    display all the cartitem with the placed status.
    """
    # import pdb;pdb.set_trace();
    if request.method == "POST":
        Cart.objects.filter(user=request.user).update(status="placed")  # update cart with the placed status
        messages.success(request, CARTITEM_PLACED_MSG)
        return redirect('view_order_list')


@login_required(login_url='/login/')
def view_order_list(request):
    """
    redirect to cart page
    """
    cart = Cart.objects.filter(user=request.user, status='placed')  # view all the record where status is placed
    return render(request, ORDER_URL, {'cart': cart})