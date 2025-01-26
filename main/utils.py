from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from main.models import User





def send_email_for_verify(request, user_name, user_email, use_https=False):
    user = User.objects.get(username=user_name)
    current_site = get_current_site(request)
    context = {
        "domain": current_site.domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        'user': user,
        "token": token_generator.make_token(user),
        "protocol": "https" if use_https else "http",
    }

    message = render_to_string(
        'main/verify_email.html',
        context=context
    )

    email = EmailMessage(
        'verify email',
        message,
        "from@example.com",
        to=[user_email],
    )
    email.send()