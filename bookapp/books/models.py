from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}" if self.middle_name else f"{self.last_name}, {self.first_name}"


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField('Book', related_name='publishers')

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    authors = models.ManyToManyField(Author, related_name='books')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='books_published')
    cover = models.ImageField(upload_to='images/')
    file_book = models.FileField(upload_to='books/')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    genres = models.ManyToManyField(Genre, related_name='books')

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, default=None)
    price = models.PositiveIntegerField(default=1)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk} - {self.user.username}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)