import os
import requests
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from menu.models import Category, MenuItem
import tempfile
import logging
import time

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Populates the database with sample menu items and categories'

    def download_image(self, url, item_name):
        """Downloads an image from URL and returns a Django File object."""
        try:
            # Add query parameters to avoid caching
            url = f"{url}?t={int(time.time())}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, stream=True, headers=headers)
            if response.status_code != 200:
                logger.error(f"Failed to download image for {item_name}: HTTP {response.status_code}")
                return None
            
            # Get the file extension from the URL
            ext = url.split('.')[-1].split('?')[0]
            if ext not in ['jpg', 'jpeg', 'png', 'webp']:
                ext = 'jpg'
            
            # Create a temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f'.{ext}')
            
            # Write the image content to the temporary file
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    temp_file.write(chunk)
            
            temp_file.flush()
            temp_file.close()  # Close the file after writing
            
            # Verify the file exists and has content
            if os.path.exists(temp_file.name) and os.path.getsize(temp_file.name) > 0:
                return temp_file.name
            else:
                logger.error(f"Downloaded file for {item_name} is empty or does not exist")
                return None
            
        except Exception as e:
            logger.error(f"Error downloading image for {item_name}: {str(e)}")
            return None

    def handle(self, *args, **options):
        # Ensure media directory exists
        menu_items_dir = os.path.join(settings.MEDIA_ROOT, 'menu_items')
        os.makedirs(menu_items_dir, exist_ok=True)

        # Sample data with categories and items
        menu_data = {
            'Starters': [
                {
                    'name': 'Crispy Spring Rolls',
                    'description': 'Crispy vegetable spring rolls served with sweet chili sauce',
                    'price': 8.99,
                    'image_url': 'https://images.unsplash.com/photo-1544025162-d76694265947'
                },
                {
                    'name': 'Buffalo Wings',
                    'description': 'Spicy chicken wings served with blue cheese dip',
                    'price': 12.99,
                    'image_url': 'https://images.unsplash.com/photo-1608039829572-78524f79c4c7'
                }
            ],
            'Pasta': [
                {
                    'name': 'Spaghetti Carbonara',
                    'description': 'Classic Roman pasta with eggs, pecorino cheese, pancetta, and black pepper',
                    'price': 16.99,
                    'image_url': 'https://images.unsplash.com/photo-1612874742237-6526221588e3'
                },
                {
                    'name': 'Fettuccine Alfredo',
                    'description': 'Creamy fettuccine pasta with parmesan cheese sauce',
                    'price': 15.99,
                    'image_url': 'https://images.unsplash.com/photo-1548247661-3d7905940716'
                },
                {
                    'name': 'Penne Arrabbiata',
                    'description': 'Spicy tomato sauce with garlic, red chili, and fresh basil',
                    'price': 14.99,
                    'image_url': 'https://images.unsplash.com/photo-1563379926898-05f4575a45d8'
                }
            ],
            'Main Course': [
                {
                    'name': 'Grilled Salmon',
                    'description': 'Fresh Atlantic salmon with lemon butter sauce',
                    'price': 24.99,
                    'image_url': 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2'
                },
                {
                    'name': 'Beef Tenderloin',
                    'description': 'Prime beef tenderloin with red wine reduction',
                    'price': 29.99,
                    'image_url': 'https://images.unsplash.com/photo-1558030006-450675393462'
                },
                {
                    'name': 'Mushroom Risotto',
                    'description': 'Creamy Arborio rice with wild mushrooms',
                    'price': 18.99,
                    'image_url': 'https://images.unsplash.com/photo-1476124369491-e7addf5db371'
                }
            ],
            'Desserts': [
                {
                    'name': 'Chocolate Lava Cake',
                    'description': 'Warm chocolate cake with molten center',
                    'price': 9.99,
                    'image_url': 'https://images.unsplash.com/photo-1606313564200-e75d5e30476c'
                },
                {
                    'name': 'Crème Brûlée',
                    'description': 'Classic French vanilla custard with caramelized sugar',
                    'price': 8.99,
                    'image_url': 'https://images.unsplash.com/photo-1470324161839-ce2bb6fa6bc3'
                }
            ]
        }

        # Create categories and menu items
        for category_name, items in menu_data.items():
            self.stdout.write(f"Creating category: {category_name}")
            category, _ = Category.objects.get_or_create(name=category_name)

            for item_data in items:
                self.stdout.write(f"Creating menu item: {item_data['name']}")
                
                # Create the menu item
                menu_item = MenuItem.objects.create(
                    category=category,
                    name=item_data['name'],
                    description=item_data['description'],
                    price=item_data['price']
                )

                # Download and save the image
                temp_file_path = self.download_image(item_data['image_url'], item_data['name'])
                if temp_file_path:
                    try:
                        # Generate a filename
                        filename = f"{item_data['name'].lower().replace(' ', '_')}.{temp_file_path.split('.')[-1]}"
                        # Save the image to the menu item
                        with open(temp_file_path, 'rb') as temp_file:
                            menu_item.image.save(filename, File(temp_file), save=True)
                            self.stdout.write(f"Saved image for {item_data['name']} to {menu_item.image.path}")
                        # Clean up the temporary file
                        os.unlink(temp_file_path)
                    except Exception as e:
                        logger.error(f"Error saving image for {item_data['name']}: {str(e)}")
                        if os.path.exists(temp_file_path):
                            try:
                                os.unlink(temp_file_path)
                            except:
                                pass

        self.stdout.write(self.style.SUCCESS('Successfully populated the menu database'))
