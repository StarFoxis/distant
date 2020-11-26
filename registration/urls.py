from django.urls import path, include
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', include('allauth.urls')),
    path('profile/', login_required(views.ProfileView.as_view()), name='profile'),
    path('edit/', login_required(views.edit), name='edit'),
    path('users/', views.UserListView.as_view(), name='users'),
    path('user/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('style/', views.StyleView.as_view(), name='style'),
]