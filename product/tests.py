from urllib.parse import urlencode
from django.test import TestCase
from django.urls import reverse
from cart.factories import CartItemFactory, CartFactory
from product.models import Category
from product.views import CART_UPDATE_MSG, PRODUCT_NOT_AVAILABLE_ERROR_MSG
from userlogin.factories import UserFactory
from product.factories import ProductFactory, ProductAPIFactory, CategoryFactory
from rest_framework.test import APITestCase, APIClient
from rest_framework import status


class BaseTest(TestCase):
    def setUp(self):
        """setup called before any testcases."""
        self.index_url = reverse('index')
        self.user = UserFactory()
        self.user.set_password(self.user.password)
        self.user.save()

        self.product = ProductFactory()
        self.product.save()

        self.cart = CartFactory(user=self.user)
        self.cart.save()

        self.client = APIClient()

        self.productAPI = ProductAPIFactory()
        self.productAPI.save()

        self.category = CategoryFactory()
        self.category.save()

        self.product_api_url_list_create = reverse('product-list-list')
        self.product_api_url_fetch_update_delete = reverse('product-list-detail', args=(self.productAPI.id,))
        self.category_api_url_list_create = reverse('category-list-list')
        self.category_api_url_fetch_update_delete = reverse('category-list-detail', args=(self.category.id, ))

        self.cartitem = CartItemFactory(cart=self.cart)
        self.cartitem.save()


class ProductTest(BaseTest):
    def test_product_page_load(self):
        """test that product page load successfully."""
        self.client.force_login(self.user)
        data = urlencode({'quantity': self.cartitem.quantity})
        url = reverse('view_product', args=(self.product.id, ))
        response = self.client.post(url, data, content_type="application/x-www-form-urlencoded")
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response, CART_UPDATE_MSG)

    def test_product_available_or_not(self):
        """test that product is available or not."""
        self.client.force_login(self.user)
        data = urlencode({'quantity': 60})
        url = reverse('view_product', args=(self.product.id, ))
        response = self.client.post(url, data, content_type="application/x-www-form-urlencoded")
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response, PRODUCT_NOT_AVAILABLE_ERROR_MSG)

    def test_add_cart_product(self):
        """test that product add into cart successfully."""
        self.client.force_login(self.user)
        url = reverse('add_to_cart', args=(self.product.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_pagination_is_String_or_not(self):
        """test the pagination."""
        response = self.client.get(reverse('product_list')+'?page=dsdf')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['products_item'].number), '1')

    def test_lists_all_products(self):
        """Get second page and confirm it has (exactly) remaining 9 items"""
        no_products = 10
        for product_id in range(no_products):
            """
            create products using product factory.
            """
            ProductFactory()
        response = self.client.get(reverse('product_list')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products_item']), 4)

    def test_products_has_next_page(self):
        """Get second page and confirm it has (exactly) remaining 9 items"""
        no_products = 20
        for product_id in range(no_products):
            ProductFactory()  # create products using product factory.
        response = self.client.get(reverse('product_list')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products_item']), 9)
        self.assertEqual(response.context['products_item'].has_next(), True)

    def test_empty_page(self):
        """test that next page is available or not if not then page is empty."""
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


class ProductAPITests(APITestCase, BaseTest):
    def test_product_api(self):
        """test that product api load successfully."""
        response = self.client.get(self.product_api_url_list_create)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_api_versioning(self):
        """test that product api load successfully using versioning."""
        response = self.client.get(reverse('v5:product-list-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_create_api(self):
        """test that product creates api work successfully."""
        response = self.client.post(self.product_api_url_list_create, data={
            'name': self.productAPI.name,
            'price': self.productAPI.price,
            'description': self.productAPI.description,
            'product_image': self.productAPI.product_image
        }, format="multipart")
        # Check if you get a 200 back:
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        # Check to see if Wishbone was created
        self.assertEqual(response.data['name'], self.productAPI.name)

    def test_product_list_api(self):
        """test particular product retrieve api."""
        response = self.client.get(self.product_api_url_fetch_update_delete, args=(self.productAPI.id, ))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.productAPI.name)

    def test_product_update_api(self):
        """test product update api."""
        response = self.client.put(self.product_api_url_fetch_update_delete, data={
            'name': 'abc',
            'price': self.productAPI.price,
            'description': self.productAPI.description,
            'product_image': self.productAPI.product_image
        }, format="multipart")
        # Check if you get a 200 back:
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        # Check to see if Wishbone was created
        self.assertNotEqual(response.data['name'], self.productAPI.name)

    def test_product_remove_api(self):
        """test product remove api"""
        response = self.client.get(self.product_api_url_fetch_update_delete, data={'id': self.productAPI.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lists_all_products_api(self):
        """
        Get second page and confirm it has (exactly) remaining 3 items and next page is available or not.
        """
        no_products = 10
        for product_id in range(no_products):
            ProductAPIFactory()  # create products using product factory.

        response = self.client.get(self.product_api_url_list_create + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.data.get('next'), None)


class CategoryAPITests(APITestCase, BaseTest):
    def test_category_api(self):
        """test that category api load successfully."""
        response = self.client.get(self.category_api_url_list_create)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_create_api(self):
        """test that category creates api work successfully."""
        response = self.client.post(self.category_api_url_list_create, data={
            'name': self.category.name
        }, format="json")
        # Check if you get a 200 back:
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        # Check to see if Wishbone was created
        self.assertEqual(response.data['name'], self.category.name)

    def test_category_list_api(self):
        """test particular category retrieve api."""
        response = self.client.get(self.category_api_url_fetch_update_delete, kwargs=(self.category.id, ))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_update_api(self):
        """test category update api."""
        response = self.client.put(self.category_api_url_fetch_update_delete, data={
            'name': 'abc'
        }, format="json")
        # Check if you get a 200 back:
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        # Check to see if abc was updated
        self.assertNotEqual(response.data['name'], self.category.name)

    def test_category_remove_api(self):
        """test category remove api"""
        response = self.client.delete(self.category_api_url_fetch_update_delete)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(pk=self.category.id).exists())