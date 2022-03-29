from django.test import TestCase
from django.urls import reverse

from cart.views import CARTITEM_DELETE_MSG, CARTITEM_UPDATED_MSG, CARTITEM_PLACED_MSG
from userlogin.factories import UserFactory
from cart.factories import CartItemFactory, CartFactory


class BaseTest(TestCase):
    def setUp(self):
        """
        setup called before any testcases.
        """
        self.index_url = reverse('index')
        self.user = UserFactory()
        self.user.set_password(self.user.password)
        self.user.save()

        self.cartitem = CartItemFactory()
        self.cartitem.save()

        self.cart = CartFactory()
        self.cart.save()


class CartTest(BaseTest):
    def test_cart_page_load(self):
        """
        test that cart page load successfully
        """
        self.client.force_login(self.user)
        response = self.client.post(reverse('cart'), {'quantity': self.cartitem.quantity})
        self.assertEqual(response.status_code, 200)

    def test_cart_item_remove_successfully(self):
        """
        test that cartitem remove successfully.
        """
        self.client.force_login(self.user)
        url = reverse('cartitem_remove', args=(self.cartitem.id,))
        response = self.client.post(url)
        self.assertTrue(response, CARTITEM_DELETE_MSG)
        self.assertTrue(response.status_code, 200)

    def test_cart_item_update(self):
        """
        test that cart item update successfully.
        """
        # import pdb;pdb.set_trace();
        self.client.force_login(self.user)
        url = reverse('cartitem_update', args=(self.cartitem.id,))
        response = self.client.post(url, data={'quantity': self.cartitem.quantity})
        self.assertTrue(response, CARTITEM_UPDATED_MSG)
        self.assertEqual(response.status_code, 200)

    def test_order_page_load_successfully(self):
        """
        test that order page load successfully.
        """
        self.client.force_login(self.user)
        url = reverse('order')
        response = self.client.post(url, data={'status': self.cart.status})
        self.assertTrue(response, CARTITEM_PLACED_MSG)
        self.assertEqual(response.status_code, 302)

    def test_view_order_list_load_successfully(self):
        """
        test that view order list page load successfully.
        """
        self.client.force_login(self.user)
        url = reverse('view_order_list')
        response = self.client.post(url, data={'user': self.user, 'status': self.cart.status})
        self.assertEqual(response.status_code, 200)