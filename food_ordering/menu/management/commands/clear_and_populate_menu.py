import os
import shutil
from django.core.management.base import BaseCommand
from menu.models import Category, MenuItem
from django.conf import settings
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Clears existing menu items and categories, then repopulates them'

    def handle(self, *args, **options):
        # Clear existing data
        self.stdout.write("Clearing existing menu items and categories...")
        MenuItem.objects.all().delete()
        Category.objects.all().delete()

        # Clear media directory for menu items
        menu_items_dir = os.path.join(settings.MEDIA_ROOT, 'menu_items')
        if os.path.exists(menu_items_dir):
            shutil.rmtree(menu_items_dir)
        
        # Create media directory if it doesn't exist
        os.makedirs(menu_items_dir, exist_ok=True)

        # Run the populate command
        self.stdout.write("Repopulating menu items...")
        call_command('populate_menu')

        self.stdout.write(self.style.SUCCESS('Successfully cleared and repopulated the menu database')) 