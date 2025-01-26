from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from config.settings import EMAIL_HOST_USER
from users.models import User
from django.contrib import auth





def send_email_for_verify(request, username, email, password, use_https=False):
    user = User.objects.create_user(username=username, email=email, password= password)
    user.save()
    auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    token=token_generator.make_token(user)
    User.objects.filter(username=username).update(token_verify=token)
    context = {
        "domain": get_current_site(request).domain, 
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        'user': user,
        "token": token,
        "protocol": "https" if use_https else "http",
    }

    message = render_to_string(
        'users/verify_email.html',
        context=context 
    )

    email_to_user = EmailMessage(
        'Verify email',
        message,
        from_email = EMAIL_HOST_USER,
        to=[email],
    )
    email_to_user.send()


def send_reset_password_mail(request, user, use_https=False):
    token=token_generator.make_token(user)
    context = {
        "domain": get_current_site(request).domain, 
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        'user': user,
        "token": token,
        "protocol": "https" if use_https else "http",
    }

    message = render_to_string(
        'users/reset_password_mail.html',
        context=context 
    )

    email_to_user = EmailMessage(
        'Reset Password',
        message,
        from_email = EMAIL_HOST_USER,
        to=[user.email],
    )
    email_to_user.send()

def custom_check_token(user, token):
    if token == user.token_verify:
        return True