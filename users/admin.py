from django.contrib import admin

from users.models import User

# Register your models here.

@admin.register(User)
class UserAdmin_(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_author', 'is_staff', 'course_count', 'is_verify']
    filter_horizontal = ['bought_course']