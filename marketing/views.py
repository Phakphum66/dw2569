from django.shortcuts import render

def dashboard(request):
    mock_campaigns = [
        {"name": "แคมเปญลดแรงแซงทะลุจอ", "status": "กำลังดำเนินการ", "budget": "50,000", "clicks": 12500, "conversions": 840},
        {"name": "แจกโค้ดส่งฟรี เดือนมิถุนายน", "status": "กำลังดำเนินการ", "budget": "20,000", "clicks": 8900, "conversions": 1200},
        {"name": "11.11 Mega Sale (เตรียมการ)", "status": "ฉบับร่าง", "budget": "500,000", "clicks": 0, "conversions": 0},
    ]
    
    context = {
        'campaigns': mock_campaigns,
    }
    return render(request, 'marketing/dashboard.html', context)
