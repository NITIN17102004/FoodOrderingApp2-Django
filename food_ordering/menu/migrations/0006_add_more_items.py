from django.db import migrations

def add_more_items(apps, schema_editor):
    Category = apps.get_model('menu', 'Category')
    MenuItem = apps.get_model('menu', 'MenuItem')
    
    # Add Pasta category if it doesn't exist
    pasta_category, _ = Category.objects.get_or_create(
        name='Pasta',
        defaults={'description': 'Delicious Italian pasta dishes made with fresh ingredients'}
    )
    
    # Add Burger category if it doesn't exist
    burger_category, _ = Category.objects.get_or_create(
        name='Burger',
        defaults={'description': 'Juicy burgers with premium ingredients'}
    )
    
    # Add Salad category if it doesn't exist
    salad_category, _ = Category.objects.get_or_create(
        name='Salad',
        defaults={'description': 'Fresh and healthy salads'}
    )
    
    # Add Dessert category if it doesn't exist
    dessert_category, _ = Category.objects.get_or_create(
        name='Dessert',
        defaults={'description': 'Sweet treats and delightful desserts'}
    )
    
    # Add Beverage category if it doesn't exist
    beverage_category, _ = Category.objects.get_or_create(
        name='Beverage',
        defaults={'description': 'Refreshing drinks and beverages'}
    )
    
    # Add Pasta dishes
    MenuItem.objects.get_or_create(
        name='Fettuccine Alfredo',
        defaults={
            'description': 'Creamy fettuccine pasta with parmesan cheese sauce',
            'price': 399.00,
            'category': pasta_category,
            'available': True
        }
    )
    
    MenuItem.objects.get_or_create(
        name='Penne Arrabbiata',
        defaults={
            'description': 'Spicy tomato sauce with garlic, red chili, and fresh basil',
            'price': 349.00,
            'category': pasta_category,
            'available': True
        }
    )
    
    # Add Burger dishes
    MenuItem.objects.get_or_create(
        name='Classic Cheeseburger',
        defaults={
            'description': 'Juicy beef patty with melted cheese, lettuce, tomato, and special sauce',
            'price': 299.00,
            'category': burger_category,
            'available': True
        }
    )
    
    MenuItem.objects.get_or_create(
        name='Veggie Supreme Burger',
        defaults={
            'description': 'Plant-based patty with fresh vegetables and signature sauce',
            'price': 279.00,
            'category': burger_category,
            'available': True
        }
    )
    
    # Add Salad dishes
    MenuItem.objects.get_or_create(
        name='Caesar Salad',
        defaults={
            'description': 'Crisp romaine lettuce, parmesan cheese, croutons, and Caesar dressing',
            'price': 249.00,
            'category': salad_category,
            'available': True
        }
    )
    
    # Add Featured Special Item
    MenuItem.objects.get_or_create(
        name='Surf and Turf Special',
        defaults={
            'description': 'Premium grilled steak and jumbo prawns served with garlic butter sauce and seasonal vegetables',
            'price': 899.00,
            'category': Category.objects.get(name='Indian Cuisine'),  # Adding to Indian Cuisine for variety
            'available': True
        }
    )
    
    # Add Dessert items
    MenuItem.objects.get_or_create(
        name='Chocolate Lava Cake',
        defaults={
            'description': 'Warm chocolate cake with a molten center, served with vanilla ice cream',
            'price': 249.00,
            'category': dessert_category,
            'available': True
        }
    )
    
    # Add Beverage items
    MenuItem.objects.get_or_create(
        name='Fresh Fruit Smoothie',
        defaults={
            'description': 'Blend of seasonal fruits with yogurt and honey',
            'price': 179.00,
            'category': beverage_category,
            'available': True
        }
    )

def remove_items(apps, schema_editor):
    MenuItem = apps.get_model('menu', 'MenuItem')
    Category = apps.get_model('menu', 'Category')
    
    # Remove specific items
    MenuItem.objects.filter(name__in=[
        'Surf and Turf Special',
        'Caesar Salad',
        'Classic Cheeseburger',
        'Veggie Supreme Burger',
        'Chocolate Lava Cake',
        'Fresh Fruit Smoothie'
    ]).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('menu', '0005_add_new_categories'),
    ]

    operations = [
        migrations.RunPython(add_more_items, remove_items),
    ] 