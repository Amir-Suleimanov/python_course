from django.db import models

from django.contrib.auth.models import AbstractUser

from pytils.translit import slugify
from autoslug import AutoSlugField


class User(AbstractUser):
    is_author = models.BooleanField(default=False, editable=True)
    course_count = models.BigIntegerField(default=0, editable=True, verbose_name='Количество курсов')
    bought_course = models.ManyToManyField('CourseCardModel', blank=True)
    email = models.EmailField(blank=False, null=False, unique=True, verbose_name='Email')
    user_photo = models.ImageField(upload_to='user_photo', blank=True, null=True, verbose_name='Фотография профиля')
    
    def __str__(self):
        return self.username





class CourseCardModel(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False, verbose_name='Название курса')
    slug = AutoSlugField(populate_from='title', unique=True, verbose_name='URL', slugify=slugify, editable=True)
    creation_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    price = models.IntegerField(blank=False, null=False, verbose_name='Цена')
    discount = models.IntegerField(verbose_name='Скидка', default=0)
    photo = models.ImageField(upload_to='photo_course/', blank=True, null=True, verbose_name='Фотография курса')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор курса'
    )

    
    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
    
    def __str__(self) -> str:
        return self.title

