from spa_app.models import ContactInfo
contact, created = ContactInfo.objects.get_or_create(id=1)
contact.address = '25 Lê Lợi, Thị trấn Khe Sanh, Hướng Hóa, Tỉnh Quảng Trị'
contact.phone = '0962 176 994'
contact.email = 'lenhi2408@gmail.com'
contact.facebook_name = 'Nhii Lê'
contact.facebook_url = 'https://www.facebook.com/share/1CMBCBMoAv/?mibextid=wwXIfr'
contact.working_hours = 'Thứ 2 - Chủ Nhật: 08:00 - 20:00'
contact.save()
print('Database updated successfully')
