from django.shortcuts import render, get_object_or_404
from .models import Category, MenuItem

def home_view(request):
    categories = Category.objects.all()  # Show all categories
    featured_items = MenuItem.objects.filter(available=True)[:6]  # Featured items
    
    context = {
        'categories': categories,
        'featured_items': featured_items,
    }
    return render(request, 'menu/home.html', context)

def menu_view(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    search_query = request.GET.get('q')
    
    items = MenuItem.objects.filter(available=True)

    if selected_category:
        items = MenuItem.objects.filter(category__name=selected_category, available=True)
    else:
        items = MenuItem.objects.filter(available=True)
    
    if selected_category:
        items = items.filter(category__name=selected_category)

    if search_query:
        items = items.filter(name__icontains=search_query)

    context = {
        'categories': categories,
        'items': items,
        'selected_category': selected_category,
        'search_query': search_query,
    }
    return render(request, 'menu/menu.html', context)

def item_detail_view(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id, available=True)
    
    context = {
        'item': item,
    }
    return render(request, 'menu/item_detail.html', context)