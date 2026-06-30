import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wichit2s.settings')
django.setup()

from inventory.models import Category, Product

def create_data():
    if Category.objects.exists() or Product.objects.exists():
        print("Data already exists!")
        return

    print("Creating categories...")
    electronics = Category.objects.create(name="Electronics", icon="fa-laptop")
    clothing = Category.objects.create(name="Clothing", icon="fa-tshirt")
    
    print("Creating products...")
    Product.objects.create(
        category=electronics,
        name="Smartphone X",
        description="Latest model smartphone with awesome features.",
        price=999.00,
        stock_quantity=50
    )
    Product.objects.create(
        category=electronics,
        name="Laptop Pro",
        description="High performance laptop for professionals.",
        price=1999.00,
        stock_quantity=20
    )
    Product.objects.create(
        category=clothing,
        name="Cotton T-Shirt",
        description="Comfortable 100% cotton t-shirt.",
        price=19.99,
        stock_quantity=200
    )
    Product.objects.create(
        category=clothing,
        name="Denim Jeans",
        description="Classic blue denim jeans.",
        price=49.99,
        stock_quantity=100
    )

    print("Successfully created mock data!")

if __name__ == "__main__":
    create_data()
