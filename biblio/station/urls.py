from users import views as userViews
from . import views
from django.urls import path
from django.contrib.auth import views as authViews
from . import views


urlpatterns = [
    path('', views.home, name='Home'),
    path('my_books/', views.my_books, name='my_books'),
    path('Admin panel', views.Admin, name='AdminPanel'),
    path('issue_book/', views.issue_book, name='issue_book'),
    path('manage_readers/', views.manage_readers, name='manage_readers'),
    path('reg/', userViews.register, name='reg'),
    path('user/', authViews.LoginView.as_view(template_name='users/user.html'), name='user'),
    path('exit/', authViews.LogoutView.as_view(template_name='users/exit.html'), name='exit'),
    path('return_book/', views.return_book, name='return_book'),
    path('read_books/', views.read_books, name='read_books'),
    path('reader_list/', views.reader_list, name='reader_list'),
    path('add_reader/', views.add_reader, name='add_reader'),
    path('edit_reader/<int:reader_id>/', views.edit_reader, name='edit_reader'),
    path('delete_reader/<int:reader_id>/', views.delete_reader, name='delete_reader'),
]