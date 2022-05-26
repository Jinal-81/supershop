import random

from django.conf import settings
from django.core.mail import send_mail


def generate_activation_code():
    """code generate for the forgot password."""
    return int(''.join([str(random.randint(0, 11)) for _ in range(6)]))


def send_verification_mail(email):
    """send mail to the user for the code in terminal with the generated code."""
    generated_code = generate_activation_code()  # call code generate method
    subject = 'email verification code'  # subject for the mail
    message = f'Your verification code:\n{generated_code}\n.'  # message for the mail(email body)
    from_email = settings.EMAIL_HOST_USER  # sender's mail
    recipient_list = [email, ]  # receiver's mail
    send_mail(subject, message, from_email, recipient_list)  # call send mail method

    return generated_code, recipient_list