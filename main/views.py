from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from main.utils import send_email_for_verify


from .models import CourseCardModel, User
from .forms import CourseCardForm, RegistrationForm, LoginForm

# Create your views here.


def home(request):
    return render(request,'main/index.html')


def login(request):

    error = ''
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = request.POST.get("email")
            password = request.POST.get("password")
            user = auth.authenticate(email=email, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main:home'))
            else:
                error = 'Такого пользователя не существует'
    form = LoginForm()
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('main:home'))
    context = {
        'form': form,
        'errors': error
    }
    return render(request,'main/login.html', context=context)


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
            user = form.save()
            # send_email_for_verify(request, user_name=form.cleaned_data['username'], user_email=form.cleaned_data['email'])
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect(reverse('main:home'))
        else:
            for error in list(form.errors.values()):
                print(request, error)
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
    return render(request, 'main/registration.html', context=context)


@login_required()
def profile(request): 
    user_courses = CourseCardModel.objects.filter(author=request.user)


    context = {
        'user_courses': user_courses,
    }
    return render(request, 'main/profile.html', context=context)


def goods_all(request):
    cards = CourseCardModel.objects.all()
    discount_price = []

    for i in cards:
        if i.discount > 0:
            discount_price.append((i.id, int(i.price - i.price/100*i.discount)))
            print(discount_price[-1][1], i.discount)
    context = {
        'cards': cards,
        'discount_price': discount_price,
    }
    return render(request, 'main/products.html', context=context)

def card_info(request, course_slug):
    return render(request, 'main/course_info.html')


@login_required
def add_course(request): 
    if request.method == "POST":
        form = CourseCardForm(request.POST, request.FILES)
        form.author = request.user
        if form.is_valid():
            course = form.save(commit=False)
            course.author = request.user
            course.save()
            course_count = request.user.course_count+1
            User.objects.filter(id=request.user.id).update(course_count=course_count)
            if not request.user.is_author:
                User.objects.filter(id=request.user.id).update(is_author=True)
            return HttpResponseRedirect(reverse('main:profile'))
    form = CourseCardForm
    context = {'form': form}

    return render(request, 'main/add_course.html', context=context)


@login_required
def delete_course(request, course_slug):
    Course = get_object_or_404(CourseCardModel,slug=course_slug)
    if Course.author == request.user:
        Course.delete()
        user = User.objects.get(id=request.user.id)
        course_count = user.course_count - 1
        User.objects.filter(id=request.user.id).update(course_count=course_count)
        if course_count == 0:
            User.objects.filter(id=request.user.id).update(is_author=False)
        return HttpResponseRedirect(reverse('main:profile'))
    return HttpResponseRedirect(reverse('main:home'))


@login_required
def edit_course(request, course_slug):
    Course = get_object_or_404(CourseCardModel, slug=course_slug)
    if request.method == "POST":
        if len(request.FILES) != 0:
            Course.photo = request.FILES['photo']
        if Course.author == request.user:
            form = CourseCardForm(request.POST, instance=Course)

            if form.is_valid():
                form.save()
                return redirect('main:profile')
    form = CourseCardForm(instance=Course)
    context = {'form': form}

    return render(request, 'main/edit_course.html', context=context)

def verify_email(request, uidb64, token):
    print('Verifying email')