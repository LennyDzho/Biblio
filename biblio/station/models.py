from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
class Book(models.Model):
    title = models.CharField('Название книги', max_length=100, default='Без названия', unique=True)
    text = models.TextField('Описание книги', default='Без описания')
    date = models.DateField('Дата выхода')
    author = models.CharField('Автор',max_length=150, default='Имя автора неизвестно')
    status_choices = [
        ('available', 'Доступна'),
        ('checked_out', 'На руках'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='available')

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'



class Reader(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Привязка к пользователю Django
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    borrowed_books = models.ManyToManyField(Book, related_name='readers', blank=True)
    read_books = models.ManyToManyField(Book, related_name='readers_read', blank=True)
