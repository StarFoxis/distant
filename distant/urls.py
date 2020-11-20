from django.urls import path
from . import views

urlpatterns = [
    path('info/', views.get_info, name='get_info'),
    path('', views.TasksListView.as_view(), name='tasks'),
    path('create/', views.CreateTaskView.as_view(), name='create'),
    path('update/<int:pk>/', views.UpdateTaskView.as_view(), name='update'),
    path('delete/<int:pk>/', views.DeleteTaskView.as_view(), name='delete'),
]