from django.contrib import admin
from .models import CourseCardModel

# Register your models here.


@admin.register(CourseCardModel)
class CourseCardAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'price', 'discount'] 
    prepopulated_fields = {'slug': ('title', )}