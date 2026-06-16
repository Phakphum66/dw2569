from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    categories = [
        {"name": "เสื้อผ้าแฟชั่น", "icon": "fas fa-tshirt"},
        {"name": "มือถือ & อุปกรณ์", "icon": "fas fa-mobile-alt"},
        {"name": "เครื่องใช้ในบ้าน", "icon": "fas fa-home"},
        {"name": "สุขภาพ & ความงาม", "icon": "fas fa-heart"},
        {"name": "คอมพิวเตอร์", "icon": "fas fa-laptop"},
        {"name": "กีฬา & กิจกรรม", "icon": "fas fa-basketball-ball"},
        {"name": "ของเล่นเด็ก", "icon": "fas fa-puzzle-piece"},
        {"name": "สัตว์เลี้ยง", "icon": "fas fa-paw"},
    ]

    products = [
        {"name": "Nike Air Zoom Mercurial Superfly 9 Elite FG - รองเท้าสตั๊ดสายสปีด", "price": "9,400", "sales": "1.5พัน", "discount": "-5%", "image_url": "/static/web_sales/img/nike_mercurial_boot_1781598964137.png"},
        {"name": "Nike Phantom GX Elite FG - รองเท้าสตั๊ดสายคอนโทรล เพิ่มความแม่นยำ", "price": "8,700", "sales": "980", "discount": "", "image_url": "/static/web_sales/img/nike_phantom_boot_1781598976698.png"},
        {"name": "Nike Tiempo Legend 10 Elite FG - หนังแท้คลาสสิก นุ่มสบายเท้า", "price": "8,500", "sales": "2.1พัน", "discount": "-10%", "image_url": "/static/web_sales/img/nike_tiempo_boot_1781598989111.png"},
        {"name": "Nike Zoom Mercurial Vapor 15 Pro FG - น้ำหนักเบา ปราดเปรียว", "price": "5,400", "sales": "3.5พัน", "discount": "-15%", "image_url": "/static/web_sales/img/nike_zoom_boot_1781599001960.png"},
        {"name": "Nike Phantom Luna Elite FG - ดีไซน์สำหรับนักเตะหญิง กระชับเป็นพิเศษ", "price": "9,400", "sales": "450", "discount": "", "image_url": "/static/web_sales/img/nike_phantom_boot_1781598976698.png"},
        {"name": "Nike Premier 3 FG - สตั๊ดหนังแท้ทรงคลาสสิก ทนทานคุ้มราคา", "price": "3,800", "sales": "5.2พัน", "discount": "-20%", "image_url": "/static/web_sales/img/nike_tiempo_boot_1781598989111.png"},
        {"name": "Nike Mercurial Superfly 9 Academy MG - สำหรับสนามหญ้าเทียมและหญ้าจริง", "price": "3,100", "sales": "8.9พัน", "discount": "", "image_url": "/static/web_sales/img/nike_mercurial_boot_1781598964137.png"},
        {"name": "Nike Phantom GX Academy TF - รองเท้าร้อยปุ่มสายคอนโทรล", "price": "2,900", "sales": "4.1พัน", "discount": "-10%", "image_url": "/static/web_sales/img/nike_phantom_boot_1781598976698.png"},
        {"name": "Nike Tiempo Legend 10 Academy IC - รองเท้าฟุตซอลพื้นเรียบ", "price": "2,700", "sales": "6.3พัน", "discount": "", "image_url": "/static/web_sales/img/nike_tiempo_boot_1781598989111.png"},
        {"name": "Nike Zoom Mercurial Vapor 15 Elite SG-Pro Anti-Clog - สำหรับสนามแฉะ", "price": "10,200", "sales": "200", "discount": "-5%", "image_url": "/static/web_sales/img/nike_zoom_boot_1781599001960.png"},
    ]

    context = {
        "categories": categories,
        "products": products,
    }
    return render(request, 'web_sales/home.html', context)
