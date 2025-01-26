from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


# from users.models import User
from main.models import CourseCardModel
from .forms import CourseCardForm

# Create your views here.

User = auth.get_user_model()

def home(request):
    return render(request,'main/index.html')


def goods_all(request):
    cards = CourseCardModel.objects.all()
    discount_price = []

    for i in cards:
        if i.discount > 0:
            discount_price.append((i.id, int(i.price - i.price/100*i.discount)))
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
            return HttpResponseRedirect(reverse('users:profile'))
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
        return HttpResponseRedirect(reverse('users:profile'))
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
                return redirect('users:profile')
    form = CourseCardForm(instance=Course)
    context = {'form': form}

    return render(request, 'main/edit_course.html', context=context)

