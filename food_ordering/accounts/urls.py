from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', login_required(views.profile_view), name='profile'),
]