# ваш_проект/your_app/urls.py
from django.contrib.auth.views import LogoutView
from django.urls import path

from books import views
from books.views import BookListView, BookDetailView, buy_book_view, register, user_login, book_detail, add_review, \
    user_profile, create_genre, delete_book

urlpatterns = [
    path('create-author/', views.create_author, name='create_author'),
    path('create-publisher/', views.create_publisher, name='create_publisher'),
    path('create-book/', views.create_book, name='create_book'),
    path('', views.all_books, name='all_books'),
    path('books/', BookListView.as_view(), name='book_list'),
    path('books/<int:pk>/buy/', buy_book_view, name='buy_book'),
    path('create-genre/', create_genre, name='create_genre'),

    path('book/<int:pk>/', book_detail, name='book_detail'),
    path('add_review/<int:pk>/', add_review, name='add_review'),

    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', user_profile, name='user_profile'),
    path('books/<int:book_pk>/delete/', delete_book, name='delete_book'),
]