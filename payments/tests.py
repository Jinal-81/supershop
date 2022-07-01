from unittest.mock import patch

import requests
from django.test import TestCase
from django.urls import reverse
from faker import Faker

from cart.factories import CartFactory
from payments.factories import TransactionFactory, UserFactory1, CartFactory1
from supershop import settings
from userlogin.factories import UserFactory

STRIPE_HOST_URL = 'https://checkout.stripe.com'


# Create your tests here.
class BaseTest(TestCase):
    def setUp(self):
        """
        setup called before any testcases.
        """
        self.index_url = reverse('index')  # index page url
        self.success_url = reverse('success')  # order url
        self.user = UserFactory()  # user factory.
        self.user.set_password(self.user.password)
        self.user.save()

        self.cart = CartFactory(user=self.user)  # cart factory.
        self.cart.save()

        self.transaction = TransactionFactory(user=self.user, cart=self.cart)
        self.transaction.save()


class TransactionTest(BaseTest):
    def test_create_session_url_load(self):
        """
        test that session created using transaction successfully
        """
        # import pdb; pdb.set_trace()
        self.client.force_login(self.user)
        url = reverse('create-checkout-session', args=(self.cart.pk, ))
        response = self.client.post(url, data={
            'amount': self.transaction.amount,
            'status': self.transaction.status,
            'user': self.transaction.user,
            'cart': self.transaction.cart,
            'stripe_id': self.transaction.stripe_id
        })
        self.assertIn(STRIPE_HOST_URL, response.url)
        self.assertEqual(response.status_code, 302)

    def test_transaction_detail_page_load(self):
        """test that transaction detail page load successfully."""
        self.client.force_login(self.user)  # login force fully.
        url = reverse('view_transaction', args=(self.transaction.id, ))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

    def test_transaction_page_load(self):
        """test that transaction detail page load successfully."""
        self.client.force_login(self.user)  # login force fully.
        url = reverse('transaction_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_pagination_is_String_or_not(self):
        """test the pagination."""
        self.client.force_login(self.user)  # login force fully.
        response = self.client.get(reverse('transaction_list')+'?page=dsdf')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['transactions_item'].number), '1')

    def test_empty_page(self):
        """test that next page is available or not if not then page is empty."""
        self.client.force_login(self.user)  # login force fully.
        no_transactions = 10
        fake = Faker()
        for transaction_id in range(no_transactions):
            mobile_number = fake.msisdn()[:6]
            user = UserFactory1(mobile_number=mobile_number)
            cart = CartFactory1(user=user)
            TransactionFactory(user=user, cart=cart)  # create products using product factory.
        # Get second page and confirm it has (exactly) remaining 9 items
        response = self.client.get(reverse('transaction_list')+'?page=5')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['transactions_item'].has_next(), False)

    def test_success_page_load_successfully(self):
        """test that success page load successfully."""
        self.client.force_login(self.user)  # login force fully.
        url = reverse('success')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_cancel_page_load_successfully(self):
        """test that cancel page load successfully."""
        self.client.force_login(self.user)  # login force fully.
        url = reverse('failed')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # def some_function(user):
    #     payload = {"id": "evt_1LFytwSIaGevHT0TT7SItSoW",
    #                                              "object": "event",
    #                                              "api_version": "2020-08-27",
    #                                              "created": 1656501464,
    #                                              "data": {"object": {"id": "cs_test_a1BsIj3M147dCs94bUmRq7vLgGZIYbnUywR4UvTPg4JgdNBz8LmKEaW3uT",
    #                                                "object": "checkout.session",
    #                                                "after_expiration": None,
    #                                                "allow_promotion_codes": None,
    #                                                "amount_subtotal": 250000,
    #                                                "amount_total": 250000,
    #                                                "automatic_tax": {"enabled": False, "status": None},
    #                                                "billing_address_collection": None,
    #                                                "cancel_url": "http://127.0.0.1:8000/payment/failed/?session_id={CHECKOUT_SESSION_ID}",
    #                                                "client_reference_id": None,
    #                                                "consent": None,
    #                                                "consent_collection": None,
    #                                                "currency": "inr",
    #                                                "customer": "cus_Lxujkto5j5bfbY",
    #                                                "customer_creation": "always",
    #                                                "customer_details": {"address": {"city": None,
    #                                                  "country": "IN",
    #                                                  "line1": None,
    #                                                  "line2": None,
    #                                                  "postal_code": None,
    #                                                  "state": None},
    #                                                 "email": "test10@gmail.com",
    #                                                 "name": "test10",
    #                                                 "phone": None,
    #                                                 "tax_exempt": "null",
    #                                                 "tax_ids": []},
    #                                                "customer_email": None,
    #                                                "expires_at": 1656587847,
    #                                                "livemode": False,
    #                                                "locale": None,
    #                                                "metadata": {"transaction_id": "172", "transaction_user": "137"},
    #                                                "mode": "payment",
    #                                                "payment_intent": "pi_3LFytfSIaGevHT0T1EOZFPy2",
    #                                                "payment_link": None,
    #                                                "payment_method_options": {},
    #                                                "payment_method_types": ["card"],
    #                                                "payment_status": "paid",
    #                                                "phone_number_collection": {"enabled": False},
    #                                                "recovered_from": None,
    #                                                "setup_intent": None,
    #                                                "shipping": None,
    #                                                "shipping_address_collection": None,
    #                                                "shipping_options": [],
    #                                                "shipping_rate": None,
    #                                                "status": "complete",
    #                                                "submit_type": None,
    #                                                "subscription": None,
    #                                                "success_url": "http://127.0.0.1:8000/payment/success/?session_id={CHECKOUT_SESSION_ID}",
    #                                                "total_details": {"amount_discount": 0,
    #                                                 "amount_shipping": 0,
    #                                                 "amount_tax": 0},
    #                                                "url": None}},
    #                                              "livemode": False,
    #                                              "pending_webhooks": 1,
    #                                              "request": {"id": None, "idempotency_key": None},
    #                                              "type": "checkout.session.completed"}
    #
    #     url = reverse('webhook')
    #     response = requests.get(url, params=payload)
    #
    #     if response.status_code == 200:
    #         return response.json()
    #     else:
    #         return None
    #
    # @patch("payments.views.stripe_webhook")
    # def test_webhook(self, mocked_result):
    #     """test that webhook called successfully or not."""
    #     import pdb; pdb.set_trace()
    #     self.client.force_login(self.user)
    #     endpoint_secret = settings.STRIPE_ENDPOINT_SECRET  # stripe Signing secret
    #     mocked_result.request.META = {"SHELL": "/bin/bash", "SESSION_MANAGER": "local/jinal-All-Series:@/tmp/.ICE-unix/1592,unix/jinal-All-Series:/tmp/.ICE-unix/1592", "QT_ACCESSIBILITY": "1", "COLORTERM": "truecolor", "XDG_CONFIG_DIRS": "/etc/xdg/xdg-ubuntu:/etc/xdg", "XDG_MENU_PREFIX": "gnome-", "GNOME_DESKTOP_SESSION_ID": "this-is-deprecated", "LANGUAGE": "en_IN:en", "GNOME_SHELL_SESSION_MODE": "ubuntu", "SSH_AUTH_SOCK": "/run/user/1000/keyring/ssh", "XMODIFIERS": "@im=ibus", "DESKTOP_SESSION": "ubuntu", "SSH_AGENT_PID": "1549", "GTK_MODULES": "gail:atk-bridge", "PWD": "/home/jinal/PycharmProjects/supershop", "LOGNAME": "jinal", "XDG_SESSION_DESKTOP": "ubuntu", "XDG_SESSION_TYPE": "x11", "GPG_AGENT_INFO": "/run/user/1000/gnupg/S.gpg-agent:0:1", "XAUTHORITY": "/run/user/1000/gdm/Xauthority", "GJS_DEBUG_TOPICS": "JS ERROR;JS LOG", "WINDOWPATH": "2", "HOME": "/home/jinal", "USERNAME": "jinal", "IM_CONFIG_PHASE": "1", "LANG": "en_IN", "LS_COLORS": "rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.zst=01;31:*.tzst=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.wim=01;31:*.swm=01;31:*.dwm=01;31:*.esd=01;31:*.jpg=01;35:*.jpeg=01;35:*.mjpg=01;35:*.mjpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.m4a=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.oga=00;36:*.opus=00;36:*.spx=00;36:*.xspf=00;36:", "XDG_CURRENT_DESKTOP": "ubuntu:GNOME", "VIRTUAL_ENV": "/home/jinal/PycharmProjects/CRUD/venv", "VTE_VERSION": "6003", "GNOME_TERMINAL_SCREEN": "/org/gnome/Terminal/screen/05b2e4e5_b632_4fa9_8ff0_6a3eb4dc7fe5", "INVOCATION_ID": "db28fad73a9445bcbdf66a7a1a962c05", "MANAGERPID": "1371", "GJS_DEBUG_OUTPUT": "stderr", "LESSCLOSE": "/usr/bin/lesspipe %s %s", "XDG_SESSION_CLASS": "user", "TERM": "xterm-256color", "LESSOPEN": "| /usr/bin/lesspipe %s", "USER": "jinal", "GNOME_TERMINAL_SERVICE": ":1.130", "DISPLAY": ":0", "SHLVL": "1", "QT_IM_MODULE": "ibus", "XDG_RUNTIME_DIR": "/run/user/1000", "PS1": "(venv) \\[\\e]0;\\u@\\h: \\w\\a\\]${debian_chroot:+($debian_chroot)}\\[\\033[01;32m\\]\\u@\\h\\[\\033[00m\\]:\\[\\033[01;34m\\]\\w\\[\\033[00m\\]\\$ ", "JOURNAL_STREAM": "8:39107", "XDG_DATA_DIRS": "/usr/share/ubuntu:/usr/local/share/:/usr/share/:/var/lib/snapd/desktop", "PATH": "/home/jinal/PycharmProjects/CRUD/venv/bin:/home/jinal/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin", "GDMSESSION": "ubuntu", "DBUS_SESSION_BUS_ADDRESS": "unix:path=/run/user/1000/bus", "OLDPWD": "/home/jinal/PycharmProjects", "_": "/home/jinal/PycharmProjects/CRUD/venv/bin/python", "DJANGO_SETTINGS_MODULE": "supershop.settings", "TZ": "UTC", "RUN_MAIN": "true", "SERVER_NAME": "localhost", "GATEWAY_INTERFACE": "CGI/1.1", "SERVER_PORT": "8000", "REMOTE_HOST": "", "CONTENT_LENGTH": "2364", "SCRIPT_NAME": "", "SERVER_PROTOCOL": "HTTP/1.1", "SERVER_SOFTWARE": "WSGIServer/0.2", "REQUEST_METHOD": "POST", "PATH_INFO": "/payment/webhook/stripe", "QUERY_STRING": "", "REMOTE_ADDR": "127.0.0.1", "CONTENT_TYPE": "application/json; charset=utf-8", "HTTP_HOST": "e784-103-24-180-44.ngrok.io", "HTTP_USER_AGENT": "Stripe/1.0 (+https://stripe.com/docs/webhooks)", "HTTP_ACCEPT": "*/*; q=0.5, application/xml", "HTTP_CACHE_CONTROL": "no-cache", "HTTP_STRIPE_SIGNATURE": "t=1656566569,v1=0ac7b25e7a74c2d4b68bb905f9cde08f29c5684ba34ff96536bf86606772f6b7,v0=02ecc98ea78f0cd7a6259800715798478b101b8404c4daddd45b544822e06a79", "HTTP_X_FORWARDED_FOR": "13.235.14.237", "HTTP_X_FORWARDED_PROTO": "https", "HTTP_ACCEPT_ENCODING": "gzip"}
    #     mocked_result.request.body = {"id": "evt_1LFytwSIaGevHT0TT7SItSoW",
    #                                              "object": "event",
    #                                              "api_version": "2020-08-27",
    #                                              "created": 1656501464,
    #                                              "data": {"object": {"id": "cs_test_a1BsIj3M147dCs94bUmRq7vLgGZIYbnUywR4UvTPg4JgdNBz8LmKEaW3uT",
    #                                                "object": "checkout.session",
    #                                                "after_expiration": None,
    #                                                "allow_promotion_codes": None,
    #                                                "amount_subtotal": 250000,
    #                                                "amount_total": 250000,
    #                                                "automatic_tax": {"enabled": False, "status": None},
    #                                                "billing_address_collection": None,
    #                                                "cancel_url": "http://127.0.0.1:8000/payment/failed/?session_id={CHECKOUT_SESSION_ID}",
    #                                                "client_reference_id": None,
    #                                                "consent": None,
    #                                                "consent_collection": None,
    #                                                "currency": "inr",
    #                                                "customer": "cus_Lxujkto5j5bfbY",
    #                                                "customer_creation": "always",
    #                                                "customer_details": {"address": {"city": None,
    #                                                  "country": "IN",
    #                                                  "line1": None,
    #                                                  "line2": None,
    #                                                  "postal_code": None,
    #                                                  "state": None},
    #                                                 "email": "test10@gmail.com",
    #                                                 "name": "test10",
    #                                                 "phone": None,
    #                                                 "tax_exempt": "null",
    #                                                 "tax_ids": []},
    #                                                "customer_email": None,
    #                                                "expires_at": 1656587847,
    #                                                "livemode": False,
    #                                                "locale": None,
    #                                                "metadata": {"transaction_id": "172", "transaction_user": "137"},
    #                                                "mode": "payment",
    #                                                "payment_intent": "pi_3LFytfSIaGevHT0T1EOZFPy2",
    #                                                "payment_link": None,
    #                                                "payment_method_options": {},
    #                                                "payment_method_types": ["card"],
    #                                                "payment_status": "paid",
    #                                                "phone_number_collection": {"enabled": False},
    #                                                "recovered_from": None,
    #                                                "setup_intent": None,
    #                                                "shipping": None,
    #                                                "shipping_address_collection": None,
    #                                                "shipping_options": [],
    #                                                "shipping_rate": None,
    #                                                "status": "complete",
    #                                                "submit_type": None,
    #                                                "subscription": None,
    #                                                "success_url": "http://127.0.0.1:8000/payment/success/?session_id={CHECKOUT_SESSION_ID}",
    #                                                "total_details": {"amount_discount": 0,
    #                                                 "amount_shipping": 0,
    #                                                 "amount_tax": 0},
    #                                                "url": None}},
    #                                              "livemode": False,
    #                                              "pending_webhooks": 1,
    #                                              "request": {"id": None, "idempotency_key": None},
    #                                              "type": "checkout.session.completed"}
    #
    #     # with open('/home/jinal/PycharmProjects/supershop/payments/data.json', 'r') as f:
    #     #     data = f.read()
    #     url = reverse('webhook')
    #     response = self.client.post(url, data={"endpoint_secret": endpoint_secret, "payload": mocked_result.request.body, "sig_header": mocked_result.request.META["HTTP_STRIPE_SIGNATURE"]})
    #     self.assertEqual(response.status_code, 302)

    # @patch("payment.views.CreateCheckoutSessionView.post")
    # def test_mock_response(self, mock_get, rf: RequestFactory):
    #     self.client.force_login(self.user)
    #     url = reverse('webhook')
    #     response = self.client.post(url, data={
    #         'email': "ABC"
    #     })
    #     print(response, "**************", response.url)
    #     self.assertEqual(response.status_code, 302)
        # mock_get.return_value.ok = Mock(ok=True)
        # mock_get.return_value.status_code = 400
        # mock_get.return_value.json.return_value = {}
        # request = rf.post("/webhook/stripe", data=self.payload)
        # response = stripe_webhook(request)
        #
        # expected_response = {
        #     "payload": request.body,
        #     "sig_header": request.META['HTTP_STRIPE_SIGNATURE']
        # }
        #
        # assert response.data == expected_response
        # assert response.status_code == 400