import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wichit2s.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_admin():
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin1234')
        print("Admin user created successfully!")
        print("Username: admin")
        print("Password: admin1234")
    else:
        print("Admin user already exists!")
        print("Username: admin")
        print("Password: admin1234 (or whatever you set previously)")

if __name__ == "__main__":
    create_admin()
