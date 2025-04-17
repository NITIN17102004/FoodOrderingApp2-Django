from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('subtotal',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status', 'total_amount')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__email', 'delivery_address')
    readonly_fields = ('total_amount',)
    inlines = [OrderItemInline]