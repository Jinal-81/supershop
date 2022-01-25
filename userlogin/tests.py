import datetime
from unittest import mock

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .factories import UserFactory
from .forms import EMAIL_EXISTS_MSG, USERNAME_EXISTS_MSG, MOBILE_NUMBER_EXISTS_MSG
from .models import MyUser
from .views import LOGIN_ERROR_MSG, EMAIL_INVALID_MSG, PASSWORD_RESET_MESSAGE, EMAIL_TEMPLATE_PATH, DOMAIN_NAME, \
    PROTOCOL, INVALID_EMAIL_SUBJECT

PASSWORD_RESET_URL = reverse('password_reset')
PASSWORD_RESET_DONE = reverse('password_reset_done')
USER_FIELD_INVALID_MSG = "please fill in this field"
PASSWORD_FIELD_INVALID_MSG = "please fill in this field"
LOGOUT_URL = reverse('logout')


class BaseTest(TestCase):
    def setUp(self):
        """
        setup called before any testcases.
        """
        self.login_url = reverse('login')
        self.register_url = reverse('signup')
        self.index_url = reverse('index')

        self.user = UserFactory()
        self.user.set_password(self.user.password)
        self.user.save()


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
        test that signup page load properly.
        """
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)

    def test_password_confirm_page_load_properly(self):
        """
        test that password confirms page load properly.
        """
        response = self.client.get(reverse('password_reset_confirm', kwargs={'uidb64': urlsafe_base64_encode(force_bytes(self.user.pk)), 'token': default_token_generator.make_token(self.user)}))
        # self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('password_reset/done/'))


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


class SignupTest(BaseTest):
    def test_signup_success(self):
        """
        test signup success or not.
        """
        response = self.client.post(self.register_url, {'username': self.user.username, 'password': 'abc',
                                                        'first_name': self.user.first_name, 'last_name': self.user.last_name,
                                                        'email': self.user.email, 'mobile_number': self.user.mobile_number,
                                                        'birth_date': self.user.birth_date, 'profile_pic': self.user.profile_pic})
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

    def test_logout_load(self):
        """
        check that if user click on logout than user logout successfully
        """
        response = self.client.post(LOGOUT_URL)
        self.assertTrue(response, reverse('index'))


class ProductTest(BaseTest):
    def test_product_page_load(self):
        """
        test that product page load successfully.
        """
        response = self.client.post(reverse('view_product'))
        self.assertEqual(response.status_code, 200)


class CartTest(BaseTest):
    def test_cart_page_load(self):
        """
        test that cart page load successfully
        """
        response = self.client.post(reverse('cart'))
        self.assertEqual(response.status_code, 200)