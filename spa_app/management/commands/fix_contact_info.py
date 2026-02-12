from django.core.management.base import BaseCommand
from spa_app.models import ContactInfo

class Command(BaseCommand):
    help = 'Fixes contact information encoding issues and updates details'

    def handle(self, *args, **options):
        contact, created = ContactInfo.objects.get_or_create(id=1)
        contact.address = "25 Lê Lợi, Thị trấn Khe Sanh, Hướng Hóa, Tỉnh Quảng Trị"
        contact.phone = "0962 176 994"
        contact.email = "lenhi2408@gmail.com"
        contact.facebook_name = "Nhii Lê"
        contact.facebook_url = "https://www.facebook.com/share/1CMBCBMoAv/?mibextid=wwXIfr"
        contact.working_hours = "Thứ 2 - Chủ Nhật: 08:00 - 20:00"
        contact.save()
        self.stdout.write(self.style.SUCCESS('Successfully fixed contact information encoding'))
