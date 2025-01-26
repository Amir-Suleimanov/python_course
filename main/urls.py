from django.urls import path

from .views import *

app_name = 'main'

urlpatterns = [
    path('', home, name='home'),
    path('goods/', goods_all, name='goods'),
    path('goods/<slug:course_slug>/', card_info, name='card_info'),
    path('add-course/', add_course, name='add_course'),
    path('delete_course/<slug:course_slug>/', delete_course, name='delete_course'),
    path('edit_course/<slug:course_slug>/', edit_course, name='edit_course'),
]


