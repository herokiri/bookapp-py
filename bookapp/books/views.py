from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group, User
from django.core.checks import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash

from .forms import (
    AuthorForm, PublisherForm, BookForm,
    RegistrationForm, CustomAuthenticationForm, GenreForm
)
from .models import Book, Review, Order, Genre, Author, Publisher


class IsModeratorOrAdminMixin:
    def test_func(self):
        return self.request.user.groups.filter(name__in=['moderators', 'administrators']).exists()


class CreateAuthorView(IsModeratorOrAdminMixin, CreateView):
    model = Author
    template_name = 'create_author.html'
    form_class = AuthorForm
    success_url = '/'


class CreatePublisherView(IsModeratorOrAdminMixin, CreateView):
    model = Publisher
    template_name = 'create_publisher.html'
    form_class = PublisherForm
    success_url = '/'


class CreateBookView(IsModeratorOrAdminMixin, CreateView):
    model = Book
    template_name = 'create_book.html'
    form_class = BookForm
    success_url = '/'


class AllBooksView(ListView):
    model = Book
    template_name = 'all_books.html'
    context_object_name = 'books'

    def get_queryset(self):
        sort_by = self.request.GET.get('sort', 'title')
        search_query = self.request.GET.get('search', '')
        author_filter = self.request.GET.get('author', '')
        genre_filter = self.request.GET.get('genre', '')

        books = Book.objects.all()

        if genre_filter:
            books = books.filter(genres__name=genre_filter)
        if author_filter:
            books = books.filter(authors__last_name=author_filter)

        return books.order_by(sort_by).filter(
            Q(title__icontains=search_query) | Q(authors__last_name__icontains=search_query))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['authors'] = Author.objects.values_list('last_name', flat=True).distinct()
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'


class RegisterView(CreateView):
    model = User
    template_name = 'registration/register.html'
    form_class = RegistrationForm
    success_url = '/'

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance

        regular_users_group = Group.objects.get(name='Regular Users')
        user.groups.add(regular_users_group)

        login(self.request, user)
        return response


class UserLoginView(CreateView):
    template_name = 'registration/login.html'
    form_class = CustomAuthenticationForm
    success_url = '/'


class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/')

class BuyBookView(View):
    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=self.kwargs['pk'])

        order = Order()
        order.user = request.user
        order.book = book
        order.save()

        with open(book.file_book.path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{book.file_book.name}"'
            return response

class BookDetailView(View):
    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=self.kwargs['pk'])
        reviews = book.reviews.all()

        context = {'book': book, 'reviews': reviews}
        return render(request, 'book_detail.html', context)

class AddReviewView(View):
    def post(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=self.kwargs['pk'])

        if request.user.is_authenticated:
            text = request.POST.get('text')
            rating = request.POST.get('rating')
            Review.objects.create(user=request.user, book=book, text=text, rating=rating)

        return redirect('book_detail', pk=book.pk)

class UserProfileView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        orders = Order.objects.filter(user=user, ordered_at__isnull=False)
        reviews = Review.objects.filter(user=user)

        password_change_form = PasswordChangeForm(user)

        context = {
            'user': user,
            'orders': orders,
            'reviews': reviews,
            'password_change_form': password_change_form,
        }

        return render(request, 'user_profile.html', context)

    def post(self, request, *args, **kwargs):
        user = request.user
        password_change_form = PasswordChangeForm(user, request.POST)

        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user_profile.html')
        else:
            messages.error(request, 'Please correct the error below.')

        return redirect('user_profile.html')

class CreateGenreView(IsModeratorOrAdminMixin, CreateView):
    model = Genre
    template_name = 'create_genre.html'
    form_class = GenreForm
    success_url = '/'

class DeleteBookView(IsModeratorOrAdminMixin, View):
    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=self.kwargs['book_pk'])
        return render(request, 'delete_book.html', {'book': book})

    def post(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=self.kwargs['book_pk'])
        book.delete()
        return redirect('/')
