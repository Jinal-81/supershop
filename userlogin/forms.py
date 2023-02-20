import datetime

from django import forms

from .models import MyUser, Address

USERNAME_EXISTS_MSG = "username already exists."
EMAIL_EXISTS_MSG = "email already exists."
MOBILE_NUMBER_EXISTS_MSG = "mobile_number already exists."
LANDMARK_EXISTS_MSG = "Landmark exists."
ERROR_MSG = "Please fill in this field"


class NewUserForm(forms.ModelForm):
    """
    take required fields from user and registered into system
    """
    YEARS = [x for x in range(datetime.MINYEAR, datetime.MAXYEAR)]
    password = forms.CharField(widget=forms.PasswordInput)
    birth_date = forms.DateField(widget=forms.SelectDateWidget(years=YEARS))
    profile_pic = forms.ImageField()

    def clean_username(self):
        """
        check that username is exists or not.
        """
        username = self.cleaned_data.get("username")
        if MyUser.objects.filter(username=username).exists():
            self.add_error("username", USERNAME_EXISTS_MSG)
        return username

    def clean_email(self):
        """
        check that email address is exists or not.
        """
        email = self.cleaned_data.get("email")
        if MyUser.objects.filter(email=email).exists():
            self.add_error("email", EMAIL_EXISTS_MSG)
        return email

    def clean_mobile_number(self):
        """
        check that mobile number is exists or not.
        """
        mobile_number = self.cleaned_data.get("mobile_number")
        if MyUser.objects.filter(mobile_number=mobile_number).exists():
            self.add_error("mobile_number", MOBILE_NUMBER_EXISTS_MSG)
        return mobile_number

    class Meta:
        model = MyUser
        # required fields from the model
        fields = ("username", "password", "email", "first_name", "last_name", "mobile_number", "birth_date", "profile_pic")


class UserLoginForm(forms.ModelForm):
    """
    take username and password from the user for login
    """
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        # required fields for the login process
        fields = ("username", "password")


class PasswordResetForm(forms.ModelForm):
    """
    password reset page ,take email address from user and send instruction.
    """
    email = forms.EmailField()

    class Meta:
        model = MyUser
        # required field for reset password
        fields = ("email", )


class PasswordConfirmationForm(forms.ModelForm):
    """
    password confirmation form for new password
    """
    password = forms.PasswordInput()

    class Meta:
        model = MyUser
        # required field for confirm password
        fields = ("password", )


class UpdateProfile(forms.ModelForm):
    """
    update profile
    """
    first_name = forms.CharField(error_messages={'required': ERROR_MSG, })
    last_name = forms.CharField(error_messages={'required': ERROR_MSG, })
    YEARS = [x for x in range(datetime.MINYEAR, datetime.MAXYEAR)]
    birth_date = forms.DateField(widget=forms.SelectDateWidget(years=YEARS))
    profile_pic = forms.ImageField()

    def clean_first_name(self):
        """
        check that first name is empty or not.
        """
        first_name = self.cleaned_data.get("first_name")
        if first_name == "":
            self.add_error("first_name", ERROR_MSG)
        return first_name

    def clean_last_name(self):
        """
        check that last name is empty or not.
        """
        last_name = self.cleaned_data.get("last_name")
        if last_name == "":
            self.add_error("last_name", ERROR_MSG)
        return last_name

    def clean_username(self):
        """
        check that username is empty or not.
        """
        username = self.cleaned_data.get("username")
        if username == "":
            self.add_error("username", ERROR_MSG)
        return username

    def clean_birthday(self):
        """
        check that birthday is empty or not.
        """
        birth_date = self.cleaned_data.get("birth_date")
        if birth_date == "":
            self.add_error("birth_date", ERROR_MSG)
        return birth_date

    class Meta:
        model = MyUser
        fields = ("username", "first_name", "last_name", "birth_date", "profile_pic")


class AddAddress(forms.ModelForm):
    """
    add addresses from here
    """
    class Meta:
        model = Address
        fields = ['city', 'zipcode', 'landmark', 'state', 'address_type']


class UpdateAddress(forms.ModelForm):
    """
    update Addresses
    """
    class Meta:
        model = Address
        fields = ("city", "zipcode", "landmark", "state", "address_type")


class ContactForm(forms.ModelForm):
    """form for contact."""
    class Meta:
        model = MyUser
        fields = ['username', ]

