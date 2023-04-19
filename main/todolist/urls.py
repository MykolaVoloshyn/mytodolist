from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('', TaskList.as_view(), name='main'),
    path('create_task', TaskCreate.as_view(), name='create'),
    path('update_task/<int:pk>', TaskUpdate.as_view(), name='update'),
    path('delete_task/<int:pk>', TaskDelete.as_view(), name='delete'),
]
