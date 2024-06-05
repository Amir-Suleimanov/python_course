from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, CourseCardModel

# Register your models here.

@admin.register(User)
class UserAdmin_(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_author', 'is_staff', 'course_count']
    filter_horizontal = ['bought_course']



@admin.register(CourseCardModel)
class CourseCardAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'price', 'discount'] 
    prepopulated_fields = {'slug': ('title', )}