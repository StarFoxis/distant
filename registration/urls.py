from django.urls import path, include

from . import views

urlpatterns = [
    path('', include('allauth.urls')),
    path('profile/', views.profile, name='profile'),
    path('edit/', views.edit, name='edit'),
    path('users/', views.UserListView.as_view(), name='users'),
    path('user/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
]