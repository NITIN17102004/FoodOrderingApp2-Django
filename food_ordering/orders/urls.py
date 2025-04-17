from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('confirmation/<int:order_id>/', views.order_confirmation_view, name='order_confirmation'),
    path('history/', views.order_history_view, name='order_history'),
    path('detail/<int:order_id>/', views.order_detail_view, name='order_detail'),
]