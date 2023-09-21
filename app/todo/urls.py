from django.contrib import admin
from django.urls import path, include
from todo.views import UserRegisterView, UserLoginView, \
                       TasksListView, TaskCreateView, TaskEditView, TaskDeleteView
                        
from django.contrib.auth.views import LogoutView

app_name = "todo"

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='todo:login'), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),

    path('', TasksListView.as_view(), name='index'),
    path('create', TaskCreateView.as_view(), name='create'),
    path('edit/<int:pk>', TaskEditView.as_view(), name='edit'),
    path('delete/<int:pk>', TaskDeleteView.as_view(), name='delete'),
]