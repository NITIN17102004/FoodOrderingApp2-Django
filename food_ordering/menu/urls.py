from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_view, name='menu'),
    path('item/<int:item_id>/', views.item_detail_view, name='item_detail'),
]