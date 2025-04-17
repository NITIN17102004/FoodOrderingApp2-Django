from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Order, OrderItem
from menu.models import MenuItem
from accounts.models import Profile
import json

@login_required
def cart_view(request):
    return render(request, 'orders/cart.html')

@login_required
def checkout_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        cart_data = request.POST.get('cart_data')
        cart = json.loads(cart_data)
        
        # Validate cart
        if not cart:
            messages.error(request, "Your cart is empty.")
            return redirect('cart')
        
        # Create order
        delivery_address = request.POST.get('address')
        total_amount = float(request.POST.get('total_amount'))
        
        order = Order.objects.create(
            user=request.user,
            delivery_address=delivery_address,
            total_amount=total_amount,
            status='pending'
        )
        
        # Create order items
        for item_id, details in cart.items():
            try:
                menu_item = MenuItem.objects.get(id=int(item_id))
                OrderItem.objects.create(
                    order=order,
                    menu_item=menu_item,
                    quantity=details['quantity'],
                    price=float(details['price'])
                )
            except MenuItem.DoesNotExist:
                continue
        
        messages.success(request, f"Order #{order.id} placed successfully!")
        return redirect('order_confirmation', order_id=order.id)
    
    return render(request, 'orders/checkout.html', {
        'profile': profile
    })

@login_required
def order_confirmation_view(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('order_history')
        
    return render(request, 'orders/order_confirmation.html', {
        'order': order
    })

@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {
        'orders': orders
    })

@login_required
def order_detail_view(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('order_history')
        
    return render(request, 'orders/order_detail.html', {
        'order': order
    })


# This view handles the authentication check
def checkout_auth(request):
    if request.user.is_authenticated:
        # User is logged in, redirect to checkout
        return redirect('checkout')
    else:
        # User is not logged in, redirect to login with next parameter
        messages.info(request, 'Please login to complete your checkout.')
        return redirect('login')

# Your actual checkout view (requires login)
@login_required
def checkout(request):
    # Your checkout logic here
    return render(request, 'checkout.html')
