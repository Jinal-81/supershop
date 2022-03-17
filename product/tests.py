from django.test import TestCase
from django.urls import reverse
from cart.factories import CartItemFactory
from product.views import CART_UPDATE_MSG, PRODUCT_NOT_AVAILABLE_ERROR_MSG
from userlogin.factories import UserFactory
from product.factories import ProductFactory


class BaseTest(TestCase):
    def setUp(self):
        """
        setup called before any testcases.
        """
        self.index_url = reverse('index')
        self.user = UserFactory()
        self.user.set_password(self.user.password)
        self.user.save()

        self.product = ProductFactory()
        self.product.save()

        self.cartitem = CartItemFactory()
        self.cartitem.save()


class ProductTest(BaseTest):
    def test_product_page_load(self):
        """
        test that product page load successfully.
        """
        self.client.force_login(self.user)
        url = reverse('view_product', args=(self.product.id, ))
        response = self.client.post(url, data={'quantity': self.cartitem.quantity})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response, CART_UPDATE_MSG)
        self.assertRedirects(response, reverse('cart'))

    def test_product_available_or_not(self):
        """
        test that product is available or not.
        """
        self.client.force_login(self.user)
        url = reverse('view_product', args=(self.product.id, ))
        response = self.client.post(url, data={'quantity': 60})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response, PRODUCT_NOT_AVAILABLE_ERROR_MSG)
        self.assertRedirects(response, reverse('cart'))

    def test_add_cart_product(self):
        """
        test that product add into cart successfully.
        """
        self.client.force_login(self.user)
        url = reverse('add_to_cart', args=(self.product.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


