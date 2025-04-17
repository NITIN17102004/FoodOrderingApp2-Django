from django.db import migrations

def update_prices(apps, schema_editor):
    MenuItem = apps.get_model('menu', 'MenuItem')
    
    # Update Fettuccine Alfredo
    MenuItem.objects.filter(name='Fettuccine Alfredo').update(price=399.00)
    
    # Update Penne Arrabbiata
    MenuItem.objects.filter(name='Penne Arrabbiata').update(price=349.00)
    
    # Update Grilled Salmon
    MenuItem.objects.filter(name='Grilled Salmon').update(price=599.00)
    
    # Update other items with moderate increases
    for item in MenuItem.objects.all():
        if item.price < 300:  # If price is less than ₹300
            item.price = item.price * 20  # Convert from USD to INR approximately
            item.save()

def reverse_prices(apps, schema_editor):
    MenuItem = apps.get_model('menu', 'MenuItem')
    
    # Restore original prices
    MenuItem.objects.filter(name='Fettuccine Alfredo').update(price=15.99)
    MenuItem.objects.filter(name='Penne Arrabbiata').update(price=14.99)
    MenuItem.objects.filter(name='Grilled Salmon').update(price=24.99)

class Migration(migrations.Migration):
    dependencies = [
        ('menu', '0002_review'),
    ]

    operations = [
        migrations.RunPython(update_prices, reverse_prices),
    ] 