from urllib.parse import urlencode

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from cart.factories import CartItemFactory, CartFactory
from cart.models import Cart, CartItem
from cart.views import CARTITEM_DELETE_MSG, CARTITEM_UPDATED_MSG
from product.factories import ProductFactory
from userlogin.factories import UserFactory


class BaseTest(TestCase):
    def setUp(self):
        """
        setup called before any testcases.
        """
        self.index_url = reverse('index')  # index page url
        self.order_url = reverse('order')  # order url
        self.user = UserFactory()  # user factory.
        self.user.set_password(self.user.password)
        self.user.save()

        self.cart = CartFactory(user=self.user)  # cart factory.
        self.cart.save()

        self.product = ProductFactory()  # product factory.
        self.product.save()

        self.cartitem = CartItemFactory(cart=self.cart)  # cart item factory here passed cart instance beacuse i'm getting
        # npne value for the quantity.
        self.cartitem.save()

        self.client = APIClient()  # apiclient instance for the api test cases.
        # usl's for the cart and cartitem api.
        self.cart_api_url_list_create = reverse('cart-list-list')
        self.cart_api_url_fetch_update_delete = reverse('cart-list-detail', args=(self.cart.id, ))
        self.cartitem_api_url_list_create = reverse('cartitem-list-list')
        self.cartitem_api_url_fetch_update_delete = reverse('cartitem-list-detail', args=(self.cartitem.id,))


class CartTest(BaseTest):
    def test_order_page_load(self):
        """
        test that order page load successfully
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('order'))
        self.assertEqual(response.status_code, 200)

    def test_order_page(self):
        """
        test that order page load successfully
        """
        self.client.force_login(self.user)
        response = self.client.post(reverse('order'), data={'status': self.cart.status})
        self.assertEqual(response.status_code, 302)

    def test_cart_page_load(self):
        """
        test that cart page load successfully
        """
        self.client.force_login(self.user)
        response = self.client.post(reverse('cart'), {'quantity': self.cartitem.quantity})
        self.assertEqual(response.status_code, 200)

    def test_cart_item_remove_successfully(self):
        """
        test that cart item remove successfully.
        """
        self.client.force_login(self.user)
        url = reverse('cartitem_remove', args=(self.cartitem.id,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response, CARTITEM_DELETE_MSG)

    def test_cart_item_update(self):
        """
        test that cart item update successfully.
        """
        self.client.force_login(self.user)
        data = urlencode({'quantity': self.cartitem.quantity})
        url = reverse('cartitem_update', args=(self.cartitem.id,))
        response = self.client.post(url, data, content_type="application/x-www-form-urlencoded")
        self.assertTrue(response, CARTITEM_UPDATED_MSG)
        self.assertEqual(response.status_code, 200)

    def test_cart_item_update_error(self):
        """
        test that if user entered cartitem more than available then give error.
        """
        self.client.force_login(self.user)
        data = urlencode({'quantity': 50})
        url_cart = reverse('cartitem_update', args=(self.cartitem.id,))
        response = self.client.post(url_cart, data, content_type="application/x-www-form-urlencoded")
        self.assertEqual(response.status_code, 200)


class CartAPITestcase(APITestCase, BaseTest):
    def test_cart_list_api(self):
        """test that all the cart list api call successfully."""
        self.client.force_login(self.user)
        response = self.client.get(self.cart_api_url_list_create)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cart_list_api_versioning(self):
        """test that all the cart list api call successfully using versioning"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('cart-list-list')+'?version=v2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cart_create_api(self):
        """test that cart creates api work successfully."""
        self.client.force_login(self.user)
        response = self.client.post(self.cart_api_url_list_create, data={
            'total_amount': self.cart.total_amount,
            'status': self.cart.status,
            'user': self.cart.user.id
        })
        # Check if you get a 200 back:
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        # Check to see if Wishbone was created
        self.assertEqual(response.data['status'], self.cart.status)

    def test_cart_retrieve_api(self):
        """test particular cart retrieve api."""
        self.client.force_login(self.user)
        response = self.client.get(self.cart_api_url_fetch_update_delete, kwargs=(self.cart.id, ))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cart_update_api(self):
        """test cart update api."""
        self.client.force_login(self.user)
        response = self.client.put(self.cart_api_url_fetch_update_delete, data={
            'total_amount': self.cart.total_amount,
            'status': self.cart.status,
            'user': self.cart.user.id
        })
        # Check if you get a 200 back:
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        # Check to see if abc was updated

    def test_cart_remove_api(self):
        """test cart remove api"""
        self.client.force_login(self.user)
        response = self.client.delete(self.cart_api_url_fetch_update_delete)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Cart.objects.filter(pk=self.cart.id).exists())


class CartItemAPITestcase(APITestCase, BaseTest):
    def test_cartitem_list_api(self):
        """test that all the cart list api call successfully."""
        self.client.force_login(self.user)
        response = self.client.get(self.cartitem_api_url_list_create)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cartitem_list_api_versioning(self):
        """test that all the cart list api call successfully using versioning"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('cartitem-list-list')+'?version=v2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cartitem_create_api(self):
        """test that product creates api work successfully."""
        self.client.force_login(self.user)
        response = self.client.post(self.cartitem_api_url_list_create, data={
            'price': self.cartitem.price,
            'quantity': self.cartitem.quantity,
            'cart': self.cartitem.cart.id,
            'product': self.cartitem.product.id
        })
        # Check if you get a 200 back:
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        # Check to see if Wishbone was created
        self.assertEqual(response.data['price'], self.cartitem.price)

    def test_cartitem_retrieve_api(self):
        """test particular cart item retrieve api."""
        self.client.force_login(self.user)
        response = self.client.get(self.cartitem_api_url_fetch_update_delete, kwargs=(self.cartitem.id, ))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cartitem_update_api(self):
        """test cart update api."""
        self.client.force_login(self.user)
        response = self.client.put(self.cartitem_api_url_fetch_update_delete, data={
            'price': self.cartitem.price,
            'quantity': self.cartitem.quantity,
            'cart': self.cartitem.cart.id,
            'product': self.cartitem.product.id
        })
        # Check if you get a 200 back:
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        # Check to see if abc was updated

    def test_cartitem_remove_api(self):
        """test cart item remove api"""
        self.client.force_login(self.user)
        response = self.client.delete(self.cartitem_api_url_fetch_update_delete)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CartItem.objects.filter(pk=self.cartitem.id).exists())