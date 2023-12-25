from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from books.views import (
    CreateAuthorView,
    CreatePublisherView,
    CreateBookView,
    AllBooksView,
    BuyBookView,
    CreateGenreView,
    BookDetailView,
    AddReviewView,
    UserProfileView,
    DeleteBookView,
)

urlpatterns = [
    path('create-author/', CreateAuthorView.as_view(), name='create_author'),
    path('create-publisher/', CreatePublisherView.as_view(), name='create_publisher'),
    path('create-book/', CreateBookView.as_view(), name='create_book'),
    path('', AllBooksView.as_view(), name='all_books'),
    path('books/<int:pk>/buy/', BuyBookView.as_view(), name='buy_book'),
    path('create-genre/', CreateGenreView.as_view(), name='create_genre'),

    path('book/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('add_review/<int:pk>/', AddReviewView.as_view(), name='add_review'),

    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('books/<int:book_pk>/delete/', DeleteBookView.as_view(), name='delete_book'),
]
