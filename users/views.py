# Create your views here.
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.shortcuts import render
from django.contrib import auth
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator as token_generator


from main.models import CourseCardModel
from users.utils import send_email_for_verify, send_reset_password_mail, custom_check_token


from users.models import User
from users.forms import CheckPasswordForm, RegistrationForm, LoginForm, PasswordResetFrom

User = auth.get_user_model()


def login(request, user=None):

    if user:
        # if user.is_verify:
        auth.login(request, user)
        return HttpResponseRedirect(reverse('main:home'))
        # else:
        #    error = 'Подтвердите свою почту'

    error = ''
    if request.method == "POST" and user is None:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = request.POST.get("email")
            password = request.POST.get("password")
            user = auth.authenticate(email=email, password=password)
            if user:
                # if user.is_verify:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main:home'))
                # else:
                #     error = 'Подтвердите свою почту'
            else:
                error = 'Такого пользователя не существует'

    form = LoginForm()
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('main:home'))
    context = {
        'form': form,
        'errors': error
    }
    return render(request,'users/login.html', context=context)


@login_required()
def logout(request):
    if request.user:
        auth.logout(request)
        return HttpResponseRedirect(reverse('main:home'))


def registration(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('main:home'))


    errors = {'username': '', 'email': '', 'password': ''}
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            send_email_for_verify(request, username=username, email=email, password=password)
            
            return HttpResponseRedirect(reverse('main:home'))
        else:
            for error in list(form.errors.values()):
                error = str(error)
                if 'пользовател' in error:
                    errors['username'] = error
                if 'Email' in error or 'адрес' in error: 
                    errors['email'] = error
                if 'парол' in error: 
                    errors['password'] = str(error)


    form = RegistrationForm()
    context = {
        'form': form,
        'errors': errors
    }
    return render(request, 'users/registration.html', context=context)


@login_required()
def profile(request):
    user_courses = CourseCardModel.objects.filter(author=request.user)


    context = {
        'user_courses': user_courses,
    }
    return render(request, 'users/profile.html', context=context)

def verify_email(request, uidb64, token):

    try:
        # urlsafe_base64_decode() decodes to bytestring
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (
        TypeError,
        ValueError,
        OverflowError,
        User.DoesNotExist, 
        ValidationError,
    ): user = None

    if user is not None and custom_check_token(user, token=token):
        User.objects.filter(id=user.id).update(is_verify=True)
        if not request.user.is_authenticated:
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect(reverse('main:home'))
    else:
        return render(request, 'users/invalid_verify.html')

def password_reset(request, reset=False):
    error = []

    if request.method == 'POST':
        form = PasswordResetFrom(data=request.POST)
        if form.is_valid():
            email = request.POST.get("email")
            try:
                user = User.objects.get(email=email) 
            except User.DoesNotExist:
                user = None
            if user:
                reset = True
                context = {'reset': reset}
                send_reset_password_mail(request, user=user, )
                render(request, 'users/password_reset.html', context)
            else:
                error = 'Такого пользователя не существует'
        else:
            error = 'Проверьте правильность введенных данных'

    form = PasswordResetFrom()
    context = {
        'form': form,
        'errors': error,
        'reset': reset
    }
    return render(request, 'users/password_reset.html', context)

def check_passwords(request, user):
    error = ''
    if request.method == 'POST':
        form = CheckPasswordForm(data=request.POST)
        if form.is_valid():
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            print(password1 == password2)
            if password1 == password2:
                User.objects.filter(id=user.id).update(password=password1)
                user.password = password1
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return HttpResponseRedirect(reverse('main:home'))
            else:
                error = 'Неверный пароль'
        else:
            error = 'Проверьте правильность введенных данных'
    form = CheckPasswordForm()
    context = {
        'form': form,
        'errors': error,
    }

    return render(request, 'users/password_change.html', context)

def password_reset_confirm(request, uidb64, token):
    try:
        # urlsafe_base64_decode() decodes to bytestring
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (
        TypeError,
        ValueError,
        OverflowError,
        User.DoesNotExist, 
        ValidationError,
    ): user = None

    if user is not None and token_generator.check_token(user, token):
        User.objects.filter(id=user.id).update(is_verify=True)
        
        return check_passwords(request, user)
    else:
        return render(request, 'users/invalid_reset_confirm.html')
    

@login_required()
def profile(request): 
    user_courses = CourseCardModel.objects.filter(author=request.user)
    context = {
        'user_courses': user_courses,
    }
    return render(request, 'users/profile.html', context=context)