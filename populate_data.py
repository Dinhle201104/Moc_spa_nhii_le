import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moc_spa_project.settings')
django.setup()

from spa_app.models import Category, Service

# Clear existing data
Category.objects.all().delete()

# Create Categories
categories_list = [
    "Thư giãn", "Triệt lông", "Gội đầu", "Dưỡng sinh", "Peel", 
    "Chăm sóc da", "Chăm sóc body", "Phương pháp cấy", "Tiêm meso"
]

cats = {}
for cat_name in categories_list:
    cats[cat_name] = Category.objects.create(name=cat_name)

# Create Services
services_data = [
    {"cat": "Thư giãn", "name": "Massage Body Đá Nóng", "price": 500000, "desc": "Sử dụng đá nóng núi lửa kết hợp tinh dầu giúp thư giãn cơ bắp."},
    {"cat": "Thư giãn", "name": "Xông Hơi Thảo Dược", "price": 200000, "desc": "Thải độc cơ thể với các loại thảo mộc tự nhiên."},
    {"cat": "Chăm sóc da", "name": "Chăm Sóc Da Cơ Bản", "price": 350000, "desc": "Làm sạch sâu, hút bã nhờn và đắp mặt nạ dưỡng da."},
    {"cat": "Chăm sóc da", "name": "Gói Nâng Cao", "price": 1200000, "desc": "Liệu trình trẻ hóa chuyên sâu với công nghệ cao."},
    {"cat": "Gội đầu", "name": "Gội Đầu Dưỡng Sinh", "price": 150000, "desc": "Kết hợp massage đầu, cổ, vai gáy giảm căng thẳng."},
    {"cat": "Tiêm meso", "name": "Tiêm Meso Trẻ Hóa", "price": 3500000, "desc": "Cung cấp dưỡng chất trực tiếp vào da giúp da căng bóng."},
]

for s in services_data:
    Service.objects.create(
        category=cats[s["cat"]],
        name=s["name"],
        price=s["price"],
        description=s["desc"]
    )

print("Sample data populated successfully!")
