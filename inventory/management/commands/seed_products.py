from django.core.management.base import BaseCommand
from inventory.models import Category, Product

class Command(BaseCommand):
    help = 'Seed the database with Nike products'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Clear existing data
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Create Categories
        cat_football = Category.objects.create(name="รองเท้าฟุตบอล", icon="fas fa-futbol")
        cat_sports = Category.objects.create(name="อุปกรณ์กีฬา", icon="fas fa-basketball-ball")
        Category.objects.create(name="เสื้อผ้าแฟชั่น", icon="fas fa-tshirt")
        Category.objects.create(name="มือถือ & อุปกรณ์", icon="fas fa-mobile-alt")
        Category.objects.create(name="เครื่องใช้ในบ้าน", icon="fas fa-home")

        # Create Products
        products_data = [
            {"name": "Nike Air Zoom Mercurial Superfly 9 Elite FG - รองเท้าสตั๊ดสายสปีด", "price": 9400, "sales": 1500, "discount": 5, "image_url": "/static/web_sales/img/nike_mercurial_boot_1781598964137.png", "cat": cat_football},
            {"name": "Nike Phantom GX Elite FG - รองเท้าสตั๊ดสายคอนโทรล เพิ่มความแม่นยำ", "price": 8700, "sales": 980, "discount": 0, "image_url": "/static/web_sales/img/nike_phantom_boot_1781598976698.png", "cat": cat_football},
            {"name": "Nike Tiempo Legend 10 Elite FG - หนังแท้คลาสสิก นุ่มสบายเท้า", "price": 8500, "sales": 2100, "discount": 10, "image_url": "/static/web_sales/img/nike_tiempo_boot_1781598989111.png", "cat": cat_football},
            {"name": "Nike Zoom Mercurial Vapor 15 Pro FG - น้ำหนักเบา ปราดเปรียว", "price": 5400, "sales": 3500, "discount": 15, "image_url": "/static/web_sales/img/nike_zoom_boot_1781599001960.png", "cat": cat_football},
            {"name": "Nike Phantom Luna Elite FG - ดีไซน์สำหรับนักเตะหญิง กระชับเป็นพิเศษ", "price": 9400, "sales": 450, "discount": 0, "image_url": "/static/web_sales/img/nike_phantom_boot_1781598976698.png", "cat": cat_football},
            {"name": "Nike Premier 3 FG - สตั๊ดหนังแท้ทรงคลาสสิก ทนทานคุ้มราคา", "price": 3800, "sales": 5200, "discount": 20, "image_url": "/static/web_sales/img/nike_tiempo_boot_1781598989111.png", "cat": cat_football},
            {"name": "Nike Mercurial Superfly 9 Academy MG - สำหรับสนามหญ้าเทียมและหญ้าจริง", "price": 3100, "sales": 8900, "discount": 0, "image_url": "/static/web_sales/img/nike_mercurial_boot_1781598964137.png", "cat": cat_football},
            {"name": "Nike Phantom GX Academy TF - รองเท้าร้อยปุ่มสายคอนโทรล", "price": 2900, "sales": 4100, "discount": 10, "image_url": "/static/web_sales/img/nike_phantom_boot_1781598976698.png", "cat": cat_football},
            {"name": "Nike Tiempo Legend 10 Academy IC - รองเท้าฟุตซอลพื้นเรียบ", "price": 2700, "sales": 6300, "discount": 0, "image_url": "/static/web_sales/img/nike_tiempo_boot_1781598989111.png", "cat": cat_football},
            {"name": "Nike Zoom Mercurial Vapor 15 Elite SG-Pro Anti-Clog - สำหรับสนามแฉะ", "price": 10200, "sales": 200, "discount": 5, "image_url": "/static/web_sales/img/nike_zoom_boot_1781599001960.png", "cat": cat_football},
        ]

        for p in products_data:
            Product.objects.create(
                category=p['cat'],
                name=p['name'],
                price=p['price'],
                sales_count=p['sales'],
                discount_percent=p['discount'],
                image_url=p['image_url'],
                stock_quantity=100
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database.'))
