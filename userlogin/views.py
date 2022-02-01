from django import forms
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .models import MyUser, Address
from django.contrib.auth import authenticate, login, logout
from .forms import NewUserForm, UserLoginForm, PasswordConfirmationForm, UpdateProfile, AddAddress, UpdateAddress
from django.contrib.auth.forms import PasswordResetForm

LOGIN_ERROR_MSG = "Please enter valid username and password"
ACCOUNT_NOT_EXIST_MSG = 'account is not exit plz signup yourself into system'
EMAIL_TEMPLATE_PATH = 'userlogin/password/password_reset_email'
PASSWORD_RESET_MESSAGE = "Password Reset Requested"
DOMAIN_NAME = '127.0.0.1:8000'
PROTOCOL = 'http'
ADDRESS_ADDED_SUCCESSFULLY_MSG = "Add address successfully.."
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
USER_ADDRESS_URL = 'userlogin/addresses.html'
VIEW_PRODUCT_URL = "userlogin/productdetail.html"
LOGIN_SUCCESS_MSG = "login successfully.."
REGISTRATION_SUCCESS_MSG = "Registered successfully.."
USER_PROFILE_URL = 'userlogin/userprofile.html'
USER_PROFILE_UPDATE_MSG = "Your profile updated successfully.."
USER_ADDRESS_UPDATE_MSG = "Your Address update successfully.."
ADD_ADDRESS_URL = 'userlogin/Add_address.html'
ADDRESS_DELETED_MSG = "Address deleted successfully.."
USER_ADDRESS_UPDATE_URL = "userlogin/useraddressupdate.html"


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


def user_address_create(data: dict, user_pk):
    """
    create new address for user.
    """
    list_of_keys = ['city', 'zipcode', 'landmark', 'state', 'MyUser_id']
    dict1 = {}
    # fetch one by one key from the list
    for key in list_of_keys:
        # update value accordingly
        dict1.update({key: data.get(key)})
        # if key value is password that format is change for insert data
        if key == "MyUser_id":
            dict1.update({key: user_pk})
    # create user
    Address.objects.create(**dict1)


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


def password_reset_request(request):
    """
    password reset function for user.
    """
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']    # email of the user
            associated_users = MyUser.objects.filter(email=data)    # return queryset of particular user
            if associated_users.exists():   # check that user is existed or not
                for user in associated_users:   # fetch all the details about user
                    subject = PASSWORD_RESET_MESSAGE
                    email_template_name = EMAIL_TEMPLATE_PATH   # template path for password reset
                    user_detail = {"email": MyUser.email, 'domain': DOMAIN_NAME,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'user': MyUser, 'token': default_token_generator.make_token(user), 'protocol': PROTOCOL
                    }   # stored all the value related to user
                    email = render_to_string(email_template_name, user_detail)  # load the template and callrendermethod
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)   # send mail to user console
                    except BadHeaderError:  # rais exception if subject is not proper
                        return HttpResponse(INVALID_EMAIL_SUBJECT)
                    return redirect(PASSWORD_RESET_DONE_URL)
            messages.error(request, EMAIL_INVALID_MSG)
    password_reset_form = PasswordResetForm()   # if form method is not post then redirect to same page
    return render(request, PASSWORD_RESET_URL, {"password_reset_form": password_reset_form})


@login_required
def user_profile(request):
    """
    user can view and update their profile.
    """
    if request.method == "POST" or None:
        # update profile of request.user (that particular user's profile)
        form = UpdateProfile(request.POST or None, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()    # save form
            messages.success(request, USER_PROFILE_UPDATE_MSG)
            return redirect('index')
    form = UpdateProfile(instance=request.user)
    return render(request, USER_PROFILE_URL, {'form': form})


def user_address(request, id):
    """
    user can view their exist addresses.
    """
    address = Address.objects.filter(MyUser_id=id)  # filter record by user id
    return render(request, USER_ADDRESS_URL, {'address': address})


@login_required
def user_addresses_update(request, id):
    """
    user can update their addresses.
    """
    # if request.method == "POST" or None:
    #     # update profile of request.user (that particular user's profile)
    #     form = UpdateAddress(request.POST or None, instance=request.user)
    #     if form.is_valid():
    #         form.save()    # save form
    #         messages.success(request, USER_ADDRESS_UPDATE_MSG)
    #         return redirect('index')
    # form = UpdateAddress(instance=request.user)
    # return render(request, USER_ADDRESS_UPDATE_URL, {'form': form})
    address = Address.objects.get(id=id)
    form = UpdateAddress(request.POST, instance=address)
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request, USER_ADDRESS_UPDATE_URL, {'address': address})


def add_address(request):
    """
    add new address.
    """
    if request.method == 'POST' or None:
        form = AddAddress(request.POST or None)
        if form.is_valid():
            # called user create function for new user
            user_pk = request.user
            user_address_create(form.cleaned_data, user_pk)
            # display message after successfully registration
            messages.success(request, ADDRESS_ADDED_SUCCESSFULLY_MSG)
            # redirect to index page
            return redirect('index')
        # messages.error(request, FORM_NOT_VALID)
        return render(request, ADD_ADDRESS_URL, {'form': form})
    form = AddAddress()
    return render(request, ADD_ADDRESS_URL, {'form': form})


def remove_address(request, id):
    """
    user cane able to remove address from the addresses.
    """
    address = Address.objects.get(id=id)  # compare id
    address.delete()  # delete record from particular id
    messages.error(request, ADDRESS_DELETED_MSG)  # give message to user
    return redirect("index")  # redirect to index page


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

