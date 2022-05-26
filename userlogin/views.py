import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt

from product.filters import ProductFilter
from product.models import Product, Category
from .forms import NewUserForm, UserLoginForm, UpdateProfile, AddAddress
from .models import MyUser, Address

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
CATEGORY_URL = "userlogin/Homepage.html"
EMAIL_INVALID_MSG = "Email is not valid, please enter registered email"
USER_ADDRESS_URL = 'userlogin/addresses.html'
USER_ADD_ADDRESS_URL = 'userlogin/addresses.html'
VIEW_PRODUCT_URL = "userlogin/productdetail.html"
LOGIN_SUCCESS_MSG = "login successfully.."
REGISTRATION_SUCCESS_MSG = "Registered successfully.."
USER_PROFILE_URL = 'userlogin/userprofile.html'
USER_PROFILE_UPDATE_MSG = "Your profile updated successfully.."
USER_ADDRESS_UPDATE_MSG = "Your Address update successfully.."
ADDRESS_DELETED_MSG = "Address deleted successfully.."
USER_ADDRESS_UPDATE_URL = "userlogin/useraddressupdate.html"
PRODUCT_LIST_LOG_MSG = 'product list load successfully'
PAGE_NOT_INTEGER_LOG_MSG = 'page is not an integer'
PAGE_EMPTY_LOG_MSG = 'page is empty'
INDEX_PAGE_LOAD_LOG_MSG = 'INDEX page load successfully'
LOGIN_PAGE_LOAD_LOG_MSG = 'Login page load successfully.'
SIGNUP_PAGE_LOAD_LOG_MSG = 'Signup page load successfully.'
PASSWORD_RESET_PAGE_LOAD_LOG_MSG = 'Password Reset page load successfully.'
PROFILE_PAGE_LOAD_LOG_MSG = 'Profile page load successfully.'
USER_ADDRESS_PAGE_LOAD_LOG_MSG = 'User address page load successfully.'
ADDRESS_UPDATE_LOG_MSG = 'address updated successfully.'
PRODUCT_FILTER_CATEGORY_WISE = 'Filter Products Category wise.'

userlogin_info_logger = logging.getLogger('userlogin_info')
userlogin_info_logger.info('log into userlogin app.')

userlogin_debug_logger = logging.getLogger('userlogin_debug')
userlogin_debug_logger.debug('log into userlogin app.')

userlogin_warning_logger = logging.getLogger('userlogin_warning')
userlogin_warning_logger.warning('log into userlogin app.')


def index(request):
    """
    redirect to main page(index page) and filter product by their name.
    """
    categories = Category.objects.all()  # fetch all the categories.
    products = Product.objects.all().order_by('id')  # fetch all the products
    user_filter = ProductFilter(request.POST, queryset=products)  # filter product by their name
    products = user_filter.qs  # filtered result
    page = request.GET.get('page', 1)  # get the page

    paginator = Paginator(products, 3)  # tell the paginator to paginate products queryset in 3 products per page
    try:
        products_item = paginator.page(page)
        userlogin_info_logger.info(PRODUCT_LIST_LOG_MSG)
    except PageNotAnInteger:
        products_item = paginator.page(1)  # if page is not integer
        userlogin_warning_logger.warning(PAGE_NOT_INTEGER_LOG_MSG)
    except EmptyPage:
        products_item = paginator.page(paginator.num_pages)  # if page is empty.
        userlogin_warning_logger.warning(PAGE_EMPTY_LOG_MSG)
    userlogin_info_logger.info(INDEX_PAGE_LOAD_LOG_MSG)
    return render(request, INDEX_URL, {'filter': user_filter, 'categories': categories, 'products_item': products_item})


def category_search(request, id):
    """
    search product category wise
    """
    categories = Category.objects.all()  # fetch all the categories.
    categories_filter = Category.objects.get(id=id)  # fetch all the categories.
    products = Product.objects.filter(category=categories_filter).order_by('id')  # fetch all the products
    userlogin_info_logger.info(PRODUCT_FILTER_CATEGORY_WISE)
    user_filter = ProductFilter(request.POST, queryset=products)  # filter product by their name
    products = user_filter.qs  # filtered result
    page = request.GET.get('page', 1)  # get the page

    paginator = Paginator(products, 3)  # tell the paginator to paginate products queryset in 3 products per page
    try:
        products_item = paginator.page(page)
        userlogin_info_logger.info(PRODUCT_LIST_LOG_MSG)
    except PageNotAnInteger:
        products_item = paginator.page(1)  # if page is not integer
        userlogin_warning_logger.warning(PAGE_NOT_INTEGER_LOG_MSG)
    except EmptyPage:
        products_item = paginator.page(paginator.num_pages)  # if page is empty.
        userlogin_warning_logger.warning(PAGE_EMPTY_LOG_MSG)
    userlogin_info_logger.info(INDEX_PAGE_LOAD_LOG_MSG)
    return render(request, INDEX_URL, {'filter': user_filter, 'products_item': products_item, 'categories': categories})


def user_create(data: dict) -> None:
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


@csrf_exempt
def user_address_create(data: dict, user_pk):
    """
    create new address for user.
    """
    list_of_keys = ['city', 'zipcode', 'landmark', 'state', 'address_type', 'user']
    dict1 = {}
    # fetch one by one key from the list
    for key in list_of_keys:
        # update value accordingly
        dict1.update({key: data.get(key)})
        # print(dict1)
        # if key value is password that format is change for insert data
        if key == "user":
            dict1.update({key: user_pk})
            # print(user_pk)
    # create user
    return Address.objects.create(**dict1)


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
            userlogin_info_logger.info(LOGIN_SUCCESS_MSG)
            messages.success(request, LOGIN_SUCCESS_MSG)
            return redirect('index')
        else:
            # print msg that user or account is not exist
            userlogin_warning_logger.warning(LOGIN_ERROR_MSG)
            messages.error(request, LOGIN_ERROR_MSG)
    form = UserLoginForm()
    userlogin_debug_logger.debug(LOGIN_PAGE_LOAD_LOG_MSG)
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
            userlogin_info_logger.info(REGISTRATION_SUCCESS_MSG)
            messages.success(request, REGISTRATION_SUCCESS_MSG)
            # redirect to login page
            return redirect('login')
        # messages.error(request, FORM_NOT_VALID)
        userlogin_debug_logger.debug(SIGNUP_PAGE_LOAD_LOG_MSG)
        return render(request, SIGNUP_URL, {'register_form': form})
    form = NewUserForm()
    userlogin_debug_logger.debug(SIGNUP_PAGE_LOAD_LOG_MSG)
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
                                   'user': MyUser, 'token': default_token_generator.make_token(user),
                                   'protocol': PROTOCOL
                                   }   # stored all the value related to user
                    email = render_to_string(email_template_name, user_detail)  # load the template and callrendermethod
                    try:  # send mail to user console
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:  # rais exception if subject is not proper
                        userlogin_warning_logger.warning(INVALID_EMAIL_SUBJECT)
                        return HttpResponse(INVALID_EMAIL_SUBJECT)
                    userlogin_debug_logger.debug(PASSWORD_RESET_PAGE_LOAD_LOG_MSG)
                    return redirect(PASSWORD_RESET_DONE_URL)
            userlogin_warning_logger.warning(EMAIL_INVALID_MSG)
            messages.error(request, EMAIL_INVALID_MSG)
    password_reset_form = PasswordResetForm()   # if form method is not post then redirect to same page
    userlogin_debug_logger.debug(PASSWORD_RESET_PAGE_LOAD_LOG_MSG)
    return render(request, PASSWORD_RESET_URL, {"password_reset_form": password_reset_form})


@login_required(login_url='/login/')
def user_profile(request):
    """
    user can view and update their profile.
    """
    if request.method == "POST" or None:
        # update profile of request.user (that particular user's profile)
        form = UpdateProfile(request.POST or None, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()    # save form
            userlogin_info_logger.info(USER_PROFILE_UPDATE_MSG)
            messages.success(request, USER_PROFILE_UPDATE_MSG)
            return redirect('profile')
    form = UpdateProfile(instance=request.user)
    userlogin_debug_logger.debug(PROFILE_PAGE_LOAD_LOG_MSG)
    return render(request, USER_PROFILE_URL, {'form': form})


@csrf_exempt
@login_required(login_url='/login/')
def user_address(request):
    """
    user can view their exist addresses.
    """
    addresses = Address.objects.filter(user=request.user)  # fetch current user's addresses
    if request.method == 'POST':
        form = AddAddress(request.POST)
        if form.is_valid():
            # called address create function for new user
            user_pk = request.user
            obj = user_address_create(form.cleaned_data, user_pk)
            # print(obj, user_pk)
            address = {'id': obj.id, 'city': obj.city, 'landmark': obj.landmark, 'zipcode': obj.zipcode, 'state': obj.state, 'address_type': obj.address_type}
            # instance = form.save()
            data = {
                'address': address
            }
            # print(address)
            userlogin_debug_logger.debug('user view their address')
            return JsonResponse(data)  # send data
    form = AddAddress()
    userlogin_debug_logger.debug(USER_ADDRESS_PAGE_LOAD_LOG_MSG)
    return render(request, USER_ADDRESS_URL, {'form': form, 'addresses': addresses})


@csrf_exempt
@login_required(login_url='/login/')
def user_addresses_update(request):
    """
    user can update their addresses.
    """
    id1 = request.POST.get('id')  # fetch all the fields
    city1 = request.POST.get('city')
    landmark1 = request.POST.get('landmark')
    zipcode1 = request.POST.get('zipcode')
    state1 = request.POST.get('state')
    address_type1 = request.POST.get('address_type')
    obj = Address.objects.get(id=id1)  # by id change the field value
    obj.city = city1
    obj.landmark = landmark1
    obj.zipcode = zipcode1
    obj.state = state1
    obj.address_type = address_type1
    obj.save()
    obj.refresh_from_db()
    # pass data as jsonResponse
    address = {'id': obj.id, 'city': obj.city, 'landmark': obj.landmark, 'zipcode': obj.zipcode, 'state': obj.state, 'address_type': obj.address_type}
    data = {'address': address}
    userlogin_info_logger.info(ADDRESS_UPDATE_LOG_MSG)
    return JsonResponse(data)


@csrf_exempt
@login_required(login_url='/login/')
def remove_address(request):
    """
    user cane able to remove address from the addresses.
    """
    id1 = request.POST.get('id', None)
    Address.objects.get(id=id1).delete()  # delete record by id
    data = {
        'deleted': True,  # return true
        "id": id1
    }
    userlogin_info_logger.info(ADDRESS_DELETED_MSG)
    return JsonResponse(data)