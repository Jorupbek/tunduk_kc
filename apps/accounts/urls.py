from django.urls import path
from django.contrib.auth import views as auth_views

from apps.accounts.views import PasswordChange

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('change_password/', PasswordChange.as_view(), name='change_password'),
]
