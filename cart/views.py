from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from cart.models import Cart, CartItem
# Create your views here.

CART_HTML_PAGE_URL = "cart/carttry.html"
ORDER_HTML_PAGE_URL = 'cart/order.html'
CARTITEM_DELETE_MSG = "Cartitem deleted!"
CARTITEM_UPDATED_MSG = "quantity updated!"
CARTITEM_PLACED_MSG = "Cart placed!"


@login_required
def cart(request):
    """
    redirect to cart page
    """
    user_cart = Cart.objects.filter(user=request.user, status=Cart.StatusInCart.OPEN).first()  # filter current user's cart
    return render(request, CART_HTML_PAGE_URL, {'cart': user_cart})


@login_required
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


@csrf_exempt
@login_required
def cart_item_update(request, id):
    """
    update item quantity and update total price accordingly.
    """
    cartitem = CartItem.objects.get(id=id)  # get cart item
    cartitem.quantity = request.POST.get('quantity')  # get quantity from the user
    cartitem.quantity = int(cartitem.quantity)
    if cartitem.quantity > cartitem.product.quantity:  # if user entered quantity more than available, then give error.
        return JsonResponse({'status': 'error', 'message': f"Quantity Must be less than or equal to {cartitem.product.quantity}"})
    else:
        cartitem.cart.total_amount = cartitem.cart.total_amount + (int(cartitem.price) * int(cartitem.quantity))  # upda
        # te total price of the cart according cart item price and cart item quantity
        cartitem.save()
        return JsonResponse({'status': 'success', 'message': CARTITEM_UPDATED_MSG, 'id': id, 'quantity': cartitem.quantity, 'total_amount': cartitem.cart.total_amount})


@login_required(login_url='/login/')
def order(request):
    """
    display all the cartitem with the placed status.
    """
    if request.method == "POST":
        Cart.objects.filter(user=request.user).update(status=Cart.StatusInCart.PLACED)  # update cart with the placed
        # status
        messages.success(request, CARTITEM_PLACED_MSG)
        return redirect('order')
    return render(request, ORDER_HTML_PAGE_URL)