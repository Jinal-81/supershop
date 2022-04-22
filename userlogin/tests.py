from unittest import mock
from django.contrib.auth.tokens import default_token_generator
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from product.factories import ProductFactory, CategoryFactory
from .factories import UserFactory, AddressFactory
from .forms import EMAIL_EXISTS_MSG, USERNAME_EXISTS_MSG, MOBILE_NUMBER_EXISTS_MSG
from .views import LOGIN_ERROR_MSG, EMAIL_INVALID_MSG, INVALID_EMAIL_SUBJECT, USER_PROFILE_UPDATE_MSG,  \
    REGISTRATION_SUCCESS_MSG
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

PASSWORD_RESET_URL = reverse('password_reset')
PASSWORD_RESET_DONE = reverse('password_reset_done')
USER_FIELD_INVALID_MSG = "please fill in this field"
PASSWORD_FIELD_INVALID_MSG = "please fill in this field"
LOGOUT_URL = reverse('logout')
USER_PROFILE_UPDATE_URL = reverse('profile')
USER_ADD_ADDRESS_URL = reverse('user_address')


class BaseTest(TestCase):
    def setUp(self):
        """
        setup called before any testcases.
        """
        self.login_url = reverse('login')
        self.register_url = reverse('signup')
        self.index_url = reverse('index')
        self.update_url = reverse('profile')
        self.user = UserFactory()
        self.user.set_password(self.user.password)
        self.user.save()

        self.address = AddressFactory()
        self.address.user = self.user
        # self.address.save()

        self.products = ProductFactory()
        # self.products.save()

        self.categories = CategoryFactory()
        # self.categories.save()

        self.apiclient = APIClient()

        # self.user_api_url_list = reverse('api_user_list')
        # self.user_api_url_create = reverse('api_user_create')
        # self.user_api_url_retrieve = reverse('api_user_retrieve')
        # self.user_api_url_update = reverse('api_user_update')
        # self.user_api_url_delete = reverse('api_user_delete')


# Create your tests here.
class ViewsTestCase(BaseTest):
    def test_index_loads_properly(self):
        """
        test that index page load properly
        """
        response = self.client.get(self.index_url)
        # compare status code with 200
        self.assertEqual(response.status_code, 200)

    def test_login_load_properly(self):
        """
        test that login page load properly when user click on link.
        """
        response = self.client.get(self.login_url)
        # compare status code with 200
        self.assertEqual(response.status_code, 200)

    def test_signup_load_properly(self):
        """
        test that signup page load properly when user click on link.
        """
        response = self.client.get(self.register_url)
        # compare status code with 200
        self.assertEqual(response.status_code, 200)

    def test_password_confirm_page_load_properly(self):
        """
        test that password confirms page load properly.
        """
        response = self.client.get(
            reverse(
                'password_reset_confirm', kwargs={
                    'uidb64': urlsafe_base64_encode(force_bytes(self.user.pk)),
                    'token': default_token_generator.make_token(self.user)
                }
            )
        )
        # self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.find("set-password") != -1)

    def test_pagination_is_String_or_not(self):
        """
        test the pagination.
        """
        response = self.client.get(reverse('index')+'?page=dsdf')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['products_item'].number), '1')

    def test_lists_all_products(self):
        """
        Get second page and confirm it has (exactly) remaining 3 items
        """
        no_products = 10
        for product_id in range(no_products):
            """
            create products using product factory.
            """
            ProductFactory()
        response = self.client.get(reverse('index')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products_item']), 3)

    def test_products_has_next_page(self):
        """
        Get second page and confirm it has (exactly) remaining 3 items
        """
        no_products = 20
        for product_id in range(no_products):
            """
            create products using product factory.
            """
            ProductFactory()
        response = self.client.get(reverse('index')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products_item']), 3)
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
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('index')+'?page=5')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['products_item'].has_next(), False)


class LoginTest(BaseTest):
    def test_login_success_redirect(self):
        """
        test username and password,if correct then redirect to home page
        """
        response = self.client.post(self.login_url,
                                    {'username': self.user.username, 'password': 'abc'})
        self.assertRedirects(response, self.index_url)

    def test_login_fail_message(self):
        """
        test username and password wrong then display message to user.
        """
        response = self.client.post(self.login_url,
                                    {'username': 'xyz', 'password': 'xyz'})
        self.assertContains(response, LOGIN_ERROR_MSG)

    def test_category_search_load(self):
        """
        test that categories wise search page load properly.
        """
        self.client.force_login(self.user)
        url = reverse('category_search', args=(self.categories.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_pagination_is_String_or_not_category(self):
        """
        test the pagination.
        """
        url = reverse('category_search', args=(self.categories.id, ))
        response = self.client.get(url+'?page=dsdf')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['products_item'].number), '1')

    def test_empty_page_for_category(self):
        """
        test that next page is available or not if not then page is empty.
        """
        no_products = 10
        for product_id in range(no_products):
            """
            create products using product factory.
            """
            ProductFactory()
        # Get second page and confirm it has (exactly) remaining 3 items
        url = reverse('category_search', args=(self.categories.id, ))
        response = self.client.get(url+'?page=5')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['products_item'].has_next(), False)


class SignupTest(BaseTest):
    def test_signup_success(self):
        """
        test signup success or not.
        """
        response = self.client.post(self.register_url, {'username': self.user.username, 'password': 'abc',
                                                        'first_name': self.user.first_name, 'last_name': self.user.last_name,
                                                        'email': self.user.email, 'mobile_number': self.user.mobile_number,
                                                        'birth_date': self.user.birth_date, 'profile_pic': self.user.profile_pic})
        self.assertTrue(response, REGISTRATION_SUCCESS_MSG)
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

    def test_signup_success_redirect(self):
        """
        test that if user entered all field valid then redirect to log in.
        """
        response = self.client.post(self.register_url, {'username': 'jinal', 'password': 'abc',
                                                        'first_name': self.user.first_name, 'last_name': self.user.last_name,
                                                        'email': 'xyz@gmail.com', 'mobile_number': '9979848025',
                                                        'birth_date': self.user.birth_date, 'profile_pic': self.user.profile_pic})
        self.assertTrue(response, self.login_url)

    def test_signup_fail_redirect(self):
        """
        test that if all the fields wrong then not to redirect to next page.
        """
        response = self.client.post(self.register_url, {'username': 'xyz', 'password': 'xyz',
                                                        'first_name': self.user.first_name, 'last_name': self.user.last_name,
                                                        'email': self.user.email, 'mobile_number': self.user.mobile_number,
                                                        'birth_date': self.user.birth_date, 'profile_pic': self.user.profile_pic})
        self.assertTrue(response, self.register_url)

    def test_signup_fail_message(self):
        """
        test that if fields are not valid then display message to user.
        """
        response = self.client.post(self.register_url, {'username': self.user.username, 'password': self.user.password,
                                                        'first_name': self.user.first_name, 'last_name': self.user.last_name,
                                                        'email': self.user.email, 'mobile_number': self.user.mobile_number,
                                                        'birth_date': self.user.birth_date, 'profile_pic': self.user.profile_pic})
        self.assertTrue(response, self.register_url)

    def test_signup_fail_not_redirect(self):
        """
        test that signup fail then not redirect to another page.
        """
        response = self.client.post(self.register_url, {'username': 'xyz', 'password': 'xyz',
                                                        'first_name': 'xyz', 'last_name': 'patel',
                                                        'email': 'xyz@gmail.com', 'mobile_number': '997984842865',
                                                        'birth_date': self.user.birth_date, 'profile_pic': self.user.profile_pic})
        self.assertTrue(response, self.register_url)

    def test_username_exists(self):
        """
        check that username is exists and display message to user.
        """
        response = self.client.post(self.register_url, {'username': 'abc'})
        self.assertContains(response, USERNAME_EXISTS_MSG)

    def test_email_exists(self):
        """
        check that email address is exists and display message to user.
        """
        response = self.client.post(self.register_url, {'email': self.user.email})
        self.assertContains(response, EMAIL_EXISTS_MSG)

    def test_mobile_number_exists(self):
        """
        check that mobile number is exists and display message to user.
        """
        response = self.client.post(self.register_url, {'mobile_number': self.user.mobile_number})
        self.assertContains(response, MOBILE_NUMBER_EXISTS_MSG)


class ForgotPasswordTest(BaseTest):
    def test_forgot_password_load(self):
        """
        check that forgot password page load successfully.
        """
        response = self.client.post(PASSWORD_RESET_URL)
        self.assertEqual(response.status_code, 200)

    def test_email(self):
        """
        check that email is not exists
        """
        response = self.client.post(PASSWORD_RESET_URL, {'email': 'jinal1@gmail.com'})
        self.assertContains(response, EMAIL_INVALID_MSG)

    def test_redirect_to_next_page(self):
        """
        check that if email is exist then redirect to next page.
        """
        response = self.client.post(PASSWORD_RESET_URL, {'email': 'jinal@gmail.com'})
        self.assertRedirects(response, PASSWORD_RESET_DONE)

    @mock.patch("userlogin.views.PASSWORD_RESET_MESSAGE", "Test \n")
    def test_header_injection(self):
        """
        test that if subject is not valid then exception rais.
        """
        response = self.client.post(PASSWORD_RESET_URL, {'email': self.user.email})
        self.assertContains(response, INVALID_EMAIL_SUBJECT)


class UserProfileTest(BaseTest):
    def test_user_profile_page_load(self):
        """
        test that user profile page load properly.
        """
        self.client.force_login(self.user)
        response = self.client.get(USER_PROFILE_UPDATE_URL, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_user_profile_update_successfully(self):
        """
        test that data updated successfully.
        """
        self.client.force_login(self.user)
        response = self.client.post(USER_PROFILE_UPDATE_URL, {'first_name': 'Jinu', 'last_name': 'patel', 'username': 'jinu', 'birth_date': '10/01/2021', 'profile_pic': 'girl1.jpg'}, follow=True)
        self.assertTrue(response, USER_PROFILE_UPDATE_MSG)
        self.assertRedirects(response, USER_PROFILE_UPDATE_URL)


class UserAddressTest(BaseTest):
    def test_user_view_url_exists_addresses(self):
        """
        test that add address url.
        """
        self.client.force_login(self.user)
        self.client.enforce_csrf_checks = True
        response = self.client.get(USER_ADD_ADDRESS_URL)
        self.assertEqual(response.status_code, 200)

    def test_user_view_exists_addresses(self):
        """
        test that exist address view page load properly.
        """
        self.client.enforce_csrf_checks = True
        self.client.force_login(self.user)
        response = self.client.post(USER_ADD_ADDRESS_URL, {'city': 'anand',
                                                           'zipcode': '387110',
                                                           'landmark': 'KL Tower',
                                                           'state': 'Gujarat',
                                                           'address_type': 'home',
                                                           'user': self.user.id})
        self.assertEqual(response.status_code, 200)

    def test_user_remove_address(self):
        """
        test that address remove successfully.
        """
        self.client.force_login(self.user)
        self.client.enforce_csrf_checks = True
        url = reverse('remove_address')
        response = self.client.post(url, {'id': self.address.id})
        self.assertTrue(response.status_code, 200)

    def test_user_update_address(self):
        """
        test that user update address successfully
        """
        self.client.force_login(self.user)
        self.client.enforce_csrf_checks = True
        response = self.client.post(reverse('user_address_update'), {
                                          'id': self.address.id,
                                          'city': 'xyz',
                                          'zipcode': '147852',
                                          'landmark': 'skjdk',
                                          'state': 'gujarat',
                                          'address_type': 'home'
                                          })
        self.assertTrue(response.status_code, 200)


class UserAPITests(APITestCase, BaseTest):
    def test_user_list_api(self):
        """test that user api load successfully."""
        response = self.apiclient.get(reverse('api_user_list', args=('v1', )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_list_api_versioning(self):
        """test that user api load successfully using versioning"""
        response = self.apiclient.get(reverse('api_user_list', args=('v2', )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_create_api_versioning(self):
        """test that user creates without mobile number which is required field api work successfully."""
        response = self.apiclient.post(reverse('api_user_create', args=('v2', )), data={
            'username': 'apiiiversion',
            'password': self.user.password,
            'mobile_number': '',
            'profile_pic': self.user.profile_pic
        }, format="multipart")
        # Check if you get a 200 back:
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_create_api(self):
        """test that user creates api work successfully."""
        response = self.apiclient.post(reverse('api_user_create', args=('v1', )), data={
            'username': 'apiii',
            'password': self.user.password,
            'mobile_number': '7487120034',
            'profile_pic': self.user.profile_pic
        }, format="multipart")
        # Check if you get a 200 back:
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'apiii')

    def test_user_retrieve_api(self):
        """test particular user retrieve api."""
        response = self.apiclient.get(reverse('api_user_retrieve', args=('v1', self.user.id, )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_user_retrieve_api_versioning(self):
        """test particular user retrieve api using versioning."""
        # import pdb;pdb.set_trace();
        response = self.apiclient.get(reverse('api_user_retrieve', args=('v2', self.user.id, )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_retrieve_api_user_not_exists(self):
        """test particular user retrieve api and user is not exists then rais 404 error."""
        response = self.apiclient.get(reverse('api_user_retrieve', args=('v1', 56, )))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_update_api(self):
        """test user update api."""
        response = self.apiclient.put(reverse('api_user_update', args=('v1', self.user.id, )), data={
            'username': 'abcapii',
            'password': self.user.password,
            'mobile_number': self.user.mobile_number,
            'profile_pic': self.user.profile_pic
        }, format="multipart")
        # Check if you get a 200 back:
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        # Check to see if Wishbone was created
        self.assertNotEqual(response.data['username'], self.user.username)

    def test_user_update_api_versioning(self):
        """test user update api using versioning."""
        response = self.apiclient.put(reverse('api_user_update', args=('v2', self.user.id, )), data={
            'username': 'abcapiiversioning',
            'password': self.user.password,
            'mobile_number': self.user.mobile_number,
            'profile_pic': self.user.profile_pic
        }, format="multipart")
        # Check if you get a 200 back:
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        # Check to see if Wishbone was created
        self.assertNotEqual(response.data['username'], self.user.username)

    def test_user_update_api_versioning_rais_error(self):
        """test user update api without entering mobile number to forcefully rais error using versioning."""
        # import pdb;pdb.set_trace();
        response = self.apiclient.put(reverse('api_user_update', args=('v2', self.user.id, )), data={
            'username': '',
            'password': '',
            'mobile_number': '',
            'profile_pic': ''
        }, format="multipart")
        # Check if you get a 200 back:
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_remove_api(self):
        """test user remove api"""
        # import pdb;pdb.set_trace();
        response = self.apiclient.delete(reverse('api_user_delete', args=('v1', self.user.id, )))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AddressAPITests(APITestCase, BaseTest):
    def test_address_list_api(self):
        """test that address api load successfully."""
        response = self.apiclient.get(reverse('api_address_list', args=('v1', )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_address_list_api_versioning(self):
        """test that address api load successfully using versioning"""
        response = self.apiclient.get(reverse('api_address_list', args=('v2', )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_create_api(self):
        """test that address creates api work successfully."""
        response = self.apiclient.post(reverse('api_address_create', args=('v1', )), data={
            'city': 'apiii',
            'zipcode': self.address.zipcode,
            'landmark': self.address.landmark,
            'state': self.address.state,
            'user': self.user.id,
            'address_type': self.address.address_type
        })
        # Check if you get a 200 back:
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['city'], 'apiii')

    def test_address_retrieve_api(self):
        """test particular address retrieve api."""
        response = self.apiclient.get(reverse('api_address_retrieve', args=('v1', self.address.id, )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['city'], self.address.city)

    def test_address_update_api(self):
        """test address update api."""
        response = self.apiclient.put(reverse('api_address_update', args=('v1', self.address.id, )), data={
            'city': 'apiii',
            'zipcode': self.address.zipcode,
            'landmark': self.address.landmark,
            'state': self.address.state,
            'user': self.user.id,
            'address_type': self.address.address_type
        })
        # Check if you get a 200 back:
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        # Check to see if Wishbone was created
        self.assertNotEqual(response.data['city'], self.address.city)

    def test_address_remove_api(self):
        """test address remove api"""
        response = self.apiclient.get(reverse('api_address_delete', args=('v1', self.address.id, )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)