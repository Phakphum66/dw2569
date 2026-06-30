import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wichit2s.settings')
django.setup()

from inventory.models import Product

def update_images():
    print("Updating images...")
    
    # Update Smartphone X
    p1 = Product.objects.filter(name="Smartphone X").first()
    if p1:
        p1.image_url = "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?q=80&w=600&auto=format&fit=crop"
        p1.save()

    # Update Laptop Pro
    p2 = Product.objects.filter(name="Laptop Pro").first()
    if p2:
        p2.image_url = "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?q=80&w=600&auto=format&fit=crop"
        p2.save()

    # Update Cotton T-Shirt
    p3 = Product.objects.filter(name="Cotton T-Shirt").first()
    if p3:
        p3.image_url = "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?q=80&w=600&auto=format&fit=crop"
        p3.save()

    # Update Denim Jeans
    p4 = Product.objects.filter(name="Denim Jeans").first()
    if p4:
        p4.image_url = "https://images.unsplash.com/photo-1542272604-787c3835535d?q=80&w=600&auto=format&fit=crop"
        p4.save()

    print("Successfully updated product images!")

if __name__ == "__main__":
    update_images()
