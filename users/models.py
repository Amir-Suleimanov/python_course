from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

# from main.models import CourseCardModel

class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=False, 
        help_text= ("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
        verbose_name= "username"
    )
    is_author = models.BooleanField(default=False, editable=True)
    course_count = models.BigIntegerField(default=0, editable=True, verbose_name='Количество курсов')
    bought_course = models.ManyToManyField('main.CourseCardModel', blank=True) 
    email = models.EmailField(blank=False, null=False, unique=True, verbose_name='Email')
    user_photo = models.ImageField(upload_to='user_photo', blank=True, null=True, verbose_name='Фотография профиля')
    
    token_verify = models.CharField(max_length=100,null=True, blank=True,verbose_name='TokenVerification')
    is_verify = models.BooleanField(default=False, editable=True, verbose_name='Подтвержден')

    def __str__(self):
        return self.username