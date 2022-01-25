from django import forms
from django.contrib import auth, messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .models import MyUser
from django.contrib.auth import authenticate, login
from .forms import NewUserForm, UserLoginForm, PasswordConfirmationForm, UpdateProfile
from django.contrib.auth.forms import PasswordResetForm

LOGIN_ERROR_MSG = "Please enter valid username and password"
ACCOUNT_NOT_EXIST_MSG = 'account is not exit plz signup yourself into system'
EMAIL_TEMPLATE_PATH = 'userlogin/password/password_reset_email'
PASSWORD_RESET_MESSAGE = "Password Reset Requested"
DOMAIN_NAME = '127.0.0.1:8000'
PROTOCOL = 'http'
PASSWORD_CONFIRMATION_URL = "userlogin/password/password_reset_confirmation.html"
PASSWORD_RESET_URL = "userlogin/password/password_reset.html"
SIGNUP_URL = "userlogin/signin.html"
FORM_NOT_VALID = 'please enter valid form fields values'
INVALID_EMAIL_SUBJECT = 'Invalid header found.'
LOGIN_URL = 'userlogin/login.html'
PASSWORD_RESET_DONE_URL = '/password_reset/done/'
HOME_URL = "userlogin/Homepage.html"
INDEX_URL = "userlogin/Homepage.html"
EMAIL_INVALID_MSG = "Email is not valid, please enter registered email"
CART_URL = "userlogin/carttry.html"
VIEW_PRODUCT_URL = "userlogin/productdetail.html"
LOGIN_SUCCESS_MSG = "login successfully.."
REGISTRATION_SUCCESS_MSG = "Registered successfully.."
USER_PROFILE_URL = 'userlogin/userprofile.html'


def index(request):
    """
    redirect to main page(index page)
    """
    return render(request, INDEX_URL)


def user_create(data: dict):
    """
    create new user
    """
    list_of_keys = ['username', 'password', 'email', 'first_name', 'last_name', 'mobile_number', 'birth_date',
                    'profile_pic']
    dict1 = {}
    # fetch one by one key from the list
    for key in list_of_keys:
        # update value accordingly
        dict1.update({key: data.get(key)})
        # if key value is password that format is change for insert data
        if key == "password":
            dict1.update({key: make_password(data.get(key))})
    # create user
    MyUser.objects.create(**dict1)


def view_login(request):
    """
    login function for the user login
    """
    # variable for request.post
    some_var = request.POST
    # check that form method is post or not
    if request.method == 'POST':
        # get and stored username and password
        username = some_var.get('username')
        password = some_var.get('password')
        # call authenticate function and authenticate username and password
        user = authenticate(request, username=username, password=password)
        # check that user is not none
        if user:
            # call login method
            login(request, user)
            messages.success(request, LOGIN_SUCCESS_MSG)
            return redirect('index')
        else:
            # print msg that user or account is not exist
            messages.error(request, LOGIN_ERROR_MSG)
    form = UserLoginForm()
    return render(request, LOGIN_URL, {'form': form})


def signup(request):
    """
    registration for user.
    """
    if request.method == 'POST' or None:
        form = NewUserForm(request.POST or None, request.FILES)
        if form.is_valid():
            # called user create function for new user
            user_create(form.cleaned_data)
            # fetch users email id
            email = form.cleaned_data.get('email')
            # send mail to user for registration confirmation
            send_mail('Subject', 'Message', 'abc@lskdj.com', [email], fail_silently=False)
            # display message after successfully registration
            messages.success(request, REGISTRATION_SUCCESS_MSG)
            # redirect to login page
            return redirect('login')
        # messages.error(request, FORM_NOT_VALID)
        return render(request, SIGNUP_URL, {'register_form': form})
    form = NewUserForm()
    return render(request, SIGNUP_URL, {'register_form': form})


def view_logout(request):
    """
    logout user.
    """
    if request.method == 'POST':
        # call auth.logout
        auth.logout(request)
    return redirect('index')


def password_reset_request(request):
    """
    password reset function for user.
    """
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            # email of the user
            data = password_reset_form.cleaned_data['email']
            print(data)
            # return queryset of particular user
            associated_users = MyUser.objects.filter(email=data)
            print(associated_users)
            # check that user is existed or not
            if associated_users.exists():
                # fetch all the details about user
                for user in associated_users:
                    print(user)
                    subject = PASSWORD_RESET_MESSAGE
                    # template path for password reset
                    email_template_name = EMAIL_TEMPLATE_PATH
                    # stored all the value related to user
                    user_detail = {
                        "email": MyUser.email, 'domain': DOMAIN_NAME,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': MyUser, 'token': default_token_generator.make_token(user), 'protocol': PROTOCOL
                    }
                    print(user.pk)
                    # load the template and call render method
                    email = render_to_string(email_template_name, user_detail)
                    try:
                        # send mail to user console
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    # rais exception if subject is not proper
                    except BadHeaderError:
                        return HttpResponse(INVALID_EMAIL_SUBJECT)
                    return redirect(PASSWORD_RESET_DONE_URL)
            messages.error(request, EMAIL_INVALID_MSG)
    # if form method is not post then redirect to same page
    password_reset_form = PasswordResetForm()
    return render(request, PASSWORD_RESET_URL, {"password_reset_form": password_reset_form})


def password_confirmation_done(request):
    """
    password confirmation done form called for new password
    """
    form = PasswordConfirmationForm()
    return render(request, PASSWORD_CONFIRMATION_URL, {'form': form})


def user_profile(request):
    """
    user can view and update their profile.
    """
    if request.method == "POST" or None:
        form = UpdateProfile(request.POST or None, request.FIELS)
        
    return render(request, USER_PROFILE_URL)


def cart(request):
    """
    redirect to cart page
    """
    return render(request, CART_URL)


def view_product(request):
    """
    view available product details.
    """
    return render(request, VIEW_PRODUCT_URL)