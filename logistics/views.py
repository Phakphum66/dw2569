from django.shortcuts import render

def dashboard(request):
    mock_shipments = [
        {"tracking_id": "TH8472910023", "customer": "สมชาย ใจดี", "destination": "กรุงเทพมหานคร", "status": "กำลังนำจ่าย", "courier": "Kerry Express"},
        {"tracking_id": "TH8472910024", "customer": "สมหญิง รักสวย", "destination": "เชียงใหม่", "status": "เตรียมจัดส่ง", "courier": "J&T Express"},
        {"tracking_id": "TH8472910025", "customer": "ประเสริฐ ยอดเยี่ยม", "destination": "ภูเก็ต", "status": "จัดส่งสำเร็จ", "courier": "Flash Express"},
        {"tracking_id": "TH8472910026", "customer": "วิภาวดี สุดสวย", "destination": "ขอนแก่น", "status": "เตรียมจัดส่ง", "courier": "Kerry Express"},
    ]
    
    context = {
        'shipments': mock_shipments,
    }
    return render(request, 'logistics/dashboard.html', context)
