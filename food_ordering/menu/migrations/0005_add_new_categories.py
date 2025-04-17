from django.db import migrations

def add_new_categories(apps, schema_editor):
    Category = apps.get_model('menu', 'Category')
    MenuItem = apps.get_model('menu', 'MenuItem')

    # Add Pizza category
    pizza_category = Category.objects.create(
        name='Pizza',
        description='Delicious handcrafted pizzas with a variety of toppings'
    )

    # Add Pizza menu items
    MenuItem.objects.create(
        name='Margherita Pizza',
        description='Classic pizza with fresh tomatoes, mozzarella, basil, and olive oil',
        price=299.00,
        category=pizza_category,
        available=True
    )
    MenuItem.objects.create(
        name='Pepperoni Pizza',
        description='Traditional pizza topped with spicy pepperoni and melted cheese',
        price=349.00,
        category=pizza_category,
        available=True
    )

    # Add Indian Cuisine category
    indian_category = Category.objects.create(
        name='Indian Cuisine',
        description='Authentic Indian dishes with rich flavors and aromatic spices'
    )

    # Add Indian menu items
    MenuItem.objects.create(
        name='Butter Chicken',
        description='Tender chicken in rich, creamy tomato sauce with Indian spices',
        price=399.00,
        category=indian_category,
        available=True
    )
    MenuItem.objects.create(
        name='Paneer Tikka Masala',
        description='Grilled cottage cheese in spiced tomato gravy',
        price=349.00,
        category=indian_category,
        available=True
    )
    MenuItem.objects.create(
        name='Dal Makhani',
        description='Creamy black lentils cooked overnight with mild spices',
        price=299.00,
        category=indian_category,
        available=True
    )

def remove_new_categories(apps, schema_editor):
    Category = apps.get_model('menu', 'Category')
    Category.objects.filter(name__in=['Pizza', 'Indian Cuisine']).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('menu', '0003_update_prices'),
    ]

    operations = [
        migrations.RunPython(add_new_categories, remove_new_categories),
    ] 