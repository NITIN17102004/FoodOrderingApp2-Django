# Food Ordering System

A modern and user-friendly food ordering web application built with Django.

## Features

- 🍕 Browse menu items by categories
- 🔍 Search functionality
- 🛒 Shopping cart with local storage
- 👤 User authentication and profiles
- 📱 Responsive design
- 💳 Secure checkout process
- 📊 Order history tracking
- 🎯 Special offers and promotions

## Tech Stack

- **Backend**: Django 4.2.7
- **Frontend**: Bootstrap 5, jQuery
- **Database**: SQLite (Development), PostgreSQL (Production)
- **Authentication**: Django Allauth
- **Storage**: Django Storages with AWS S3 (for production)

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/food-ordering-system.git
cd food-ordering-system
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root with the following variables:
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

```
food_ordering/
├── food_ordering/          # Main project settings
├── menu/                   # Menu app
├── cart/                   # Cart app
├── orders/                 # Orders app
├── users/                  # Users app
├── static/                 # Static files
├── templates/              # Base templates
├── requirements.txt        # Project dependencies
└── manage.py              # Django management script
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Bootstrap for the frontend framework
- Font Awesome for icons
- Unsplash for food images 