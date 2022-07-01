import datetime
import logging

import stripe
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import redirect, render
# Create your views here.
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from stripe.error import SignatureVerificationError

from cart.models import Cart
from payments.filters import TransactionFilter
from payments.models import Transaction
from product.views import product_info_logger, \
    PRODUCT_PAGE_LOAD_LOG_MSG, product_debug_logger, VIEW_PRODUCT_LOG_MSG
from supershop import settings

# This is your test secret API key.

stripe.api_key = settings.STRIPE_SECRET_KEY
#
# YOUR_DOMAIN = 'http://localhost:8000'
#! /usr/bin/env python3.6

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""

VIEW_ALL_TRANSACTIONS_URL = "transaction_list.html"
VIEW_TRANSACTION_URL = "transaction_detail.html"
PAYMENT_FAILED_URL = 'payment_failed.html'
PAYMENT_SUCCESS_URL = 'payment_success.html'


import stripe


class CreateCheckoutSessionView(View):
    """class for the checkout session page."""
    def post(self, request,  *args, **kwargs):
        """method for payment using different methods of the stripe."""
        # import pdb;
        # pdb.set_trace()
        cart = Cart.objects.get(id=self.kwargs["pk"])  # fetch cart detail
        print("CART", cart)
        amount = int(cart.total_amount)
        YOUR_DOMAIN = "http://127.0.0.1:8000"  # domain
        transaction, created = Transaction.objects.get_or_create(cart=cart, user=cart.user, amount=amount, stripe_id=" ", status=Transaction.PENDING, date=datetime.date.today())
        transaction.save()
        # create stripe checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],  # payment method
            line_items=[{  # line items
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': cart,
                    },
                    'unit_amount': int(cart.total_amount) * 100,
                },
                'quantity': 1,
            }],
            metadata={
                "transaction_id": transaction.id,
                "transaction_user": cart.id
            },  # data which we want to send in webhook
            payment_intent_data={
                "metadata": {
                    "transaction_id": transaction.id,
                    "transaction_user": cart.id
                }
            },  # data for the failed transaction.in normal metadata we are not getting data at the failed time.
            mode='payment',
            # success url
                success_url=request.build_absolute_uri(
            reverse('success')
        ) + "?session_id={CHECKOUT_SESSION_ID}",
            # cancel url
            cancel_url=request.build_absolute_uri(reverse('failed')) + "?session_id={CHECKOUT_SESSION_ID}",
        )
        return redirect(checkout_session.url, code=302)


@csrf_exempt
def stripe_webhook(request):
    """web hok for the stripe payment.Check event of the payment and change status accordingly in transaction modal."""
    import pdb; pdb.set_trace()
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET  # stripe Signing secret
    payload = request.body  # request body send as payload
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']  # http stripe signature
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )  # stripe web hook
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # getting information of order from session
        sessionID = session["id"]
        # # grabbing id of the order created
        ID = session["metadata"]["transaction_id"]
        user_id = session["metadata"]["transaction_user"]
        # update transaction status
        Transaction.objects.filter(id=ID).update(status=Transaction.SUCCESS, stripe_id=sessionID)
        # update cart status
        Cart.objects.filter(id=user_id).update(status=Cart.StatusInCart.PLACED)
    # elif event['type'] == 'checkout.session.expired':
    elif event['type'] == 'payment_intent.payment_failed':
        # Get the object affected
        payment_intent = event['data']['object']
        # Use stored information to get an error object
        e = payment_intent['last_payment_error']
        user_id = payment_intent["metadata"]["transaction_user"]
        # # grabbing id of the order created
        ID = payment_intent["metadata"]["transaction_id"]
        # update transaction status
        Transaction.objects.filter(id=ID).update(status=Transaction.FAILED)
        # Use its type to choose a response
        if e['type'] == 'card_error':
            logging.error("A payment error occurred: {}".format(e['message']))
        elif e['type'] == 'invalid_request':
            logging.error("An invalid request occurred.")
        else:
            logging.error("Another problem occurred, maybe unrelated to Stripe")

    return HttpResponse(status=200)


#Failed view
@csrf_exempt
def PaymentFailedView(request):
    """class for success payment"""
    return render(request, PAYMENT_FAILED_URL)


#success view
@csrf_exempt
def PaymentSuccessView(request):
    """class for success payment"""
    return render(request, PAYMENT_SUCCESS_URL)


def transaction_list(request):
    """
    display all the transaction.
    """
    transactions = Transaction.objects.filter(user=request.user)  # fetch all the transactions
    user_filter = TransactionFilter(request.POST, queryset=transactions)  # filter transaction by status
    transactions = user_filter.qs  # filtered result
    page = request.GET.get('page', 1)  # get the page

    paginator = Paginator(transactions, 3)  # tell the paginator to paginate products queryset in 3 transaction per page
    try:
        transactions_item = paginator.page(page)
    except PageNotAnInteger:
        transactions_item = paginator.page(1)  # if page is not integer
    except EmptyPage:
        transactions_item = paginator.page(paginator.num_pages)  # if page is empty.
    product_info_logger.info(PRODUCT_PAGE_LOAD_LOG_MSG)
    return render(request, VIEW_ALL_TRANSACTIONS_URL, {'filter': user_filter, 'transactions_item': transactions_item})


def view_transaction(request, id):
    """
    view particular transaction details.
    """
    transaction = Transaction.objects.get(id=id)  # view the particular transaction
    return render(request, VIEW_TRANSACTION_URL, {'transaction': transaction})
