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

    def test_pagination_is_String_or_not(self):
        """
        test the pagination.
        """
        response = self.client.get(reverse('product_list')+'?page=dsdf')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['products_item'].number), '1')

    def test_lists_all_products(self):
        """
        Get second page and confirm it has (exactly) remaining 9 items
        """
        no_products = 10
        for product_id in range(no_products):
            """
            create products using product factory.
            """
            ProductFactory()
        response = self.client.get(reverse('product_list')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products_item']), 3)

    def test_products_has_next_page(self):
        """
        Get second page and confirm it has (exactly) remaining 9 items
        """
        no_products = 20
        for product_id in range(no_products):
            """
            create products using product factory.
            """
            ProductFactory()
        response = self.client.get(reverse('product_list')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products_item']), 9)
        self.assertEqual(response.context['products_item'].has_next(), True)

    def test_empty_page(self):
        """
        test that next page is available or not if not then page is empty.
        """
        no_products = 10
        for product_id in range(no_products):
            """
            create products using product factory.
            """
            ProductFactory()
        # Get second page and confirm it has (exactly) remaining 9 items
        response = self.client.get(reverse('product_list')+'?page=5')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['products_item'].has_next(), False)
