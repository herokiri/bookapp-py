# Ваш файл views.py
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from django.core.checks import register, messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django import template
from django.views.generic import CreateView, ListView, DetailView

from .forms import AuthorForm, PublisherForm, BookForm, RegistrationForm, CustomAuthenticationForm, GenreForm
from .models import Book, Review, Order, Genre, Author


def is_moderator_or_admin(user):
    return user.groups.filter(name__in=['moderators', 'administrators']).exists()


@user_passes_test(is_moderator_or_admin)
def create_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')  # Замените 'success' на имя вашего URL-шаблона для успешного создания
    else:
        form = AuthorForm()

    return render(request, 'create_author.html', {'form': form})


@user_passes_test(is_moderator_or_admin)
def create_publisher(request):
    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = PublisherForm()

    return render(request, 'create_publisher.html', {'form': form})


# views.py

@user_passes_test(is_moderator_or_admin)
def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = BookForm()

    context = {'form': form}
    return render(request, 'create_book.html', context)

def all_books(request):
    # Получаем параметры из GET-запроса
    sort_by = request.GET.get('sort', 'title')
    search_query = request.GET.get('search', '')
    author_filter = request.GET.get('author', '')

    # Фильтрация по жанру
    genre_filter = request.GET.get('genre', '')
    if genre_filter:
        books = Book.objects.filter(genres__name=genre_filter)
    else:
        books = Book.objects.all()

    # Применяем фильтрацию по фамилии автора
    if author_filter:
        books = books.filter(authors__last_name=author_filter)

    # Применяем сортировку и поиск
    books = books.order_by(sort_by).filter(Q(title__icontains=search_query) | Q(authors__last_name__icontains=search_query))

    # Получаем уникальные фамилии авторов
    authors = Author.objects.values_list('last_name', flat=True).distinct()

    context = {
        'books': books,
        'genres': Genre.objects.all(),
        'authors': authors,
    }

    return render(request, 'all_books.html', context)


class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'


class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            regular_users_group = Group.objects.get(name='Regular Users')
            user.groups.add(regular_users_group)

            login(request, user)
            return redirect('/')  # Redirect to the home page or any other desired page after registration
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')  # Redirect to the home page or any other desired page after login
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('/')  # Redirect to the home page or any other desired page after logout


@login_required(login_url='login')
def buy_book_view(request, pk):
    book = get_object_or_404(Book, pk=pk)

    order = Order()
    order.user = request.user
    order.book = book
    order.save()

    #
    with open(book.file_book.path, 'rb') as file:
        response = HttpResponse(file.read(),
                                content_type='application/pdf')  # Adjust content type based on your file type
        response['Content-Disposition'] = f'attachment; filename="{book.file_book.name}"'
        return response


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.all()  # Retrieve all reviews associated with the book

    context = {
        'book': book,
        'reviews': reviews,
    }

    return render(request, 'book_detail.html', context)


def add_review(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST' and request.user.is_authenticated:
        text = request.POST.get('text')
        Review.objects.create(user=request.user, book=book, text=text)

    return redirect('book_detail', pk=pk)


@login_required(login_url='login')
def user_profile(request):
    user = request.user
    orders = Order.objects.filter(user=user, ordered_at__isnull=False)
    reviews = Review.objects.filter(user=user)

    if request.method == 'POST':
        password_change_form = PasswordChangeForm(user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)  # Important for security
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user_profile.html')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        password_change_form = PasswordChangeForm(user)

    context = {
        'user': user,
        'orders': orders,
        'reviews': reviews,
        'password_change_form': password_change_form,
    }

    return render(request, 'user_profile.html', context)


def create_genre(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')  # Перенаправление на страницу списка жанров
    else:
        form = GenreForm()

    return render(request, 'create_genre.html', {'form': form})