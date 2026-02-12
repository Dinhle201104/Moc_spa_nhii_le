from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên nhóm dịch vụ")
    
    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.title()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Service(models.Model):
    category = models.ForeignKey(Category, related_name='services', on_delete=models.CASCADE, verbose_name="Nhóm dịch vụ")
    name = models.CharField(max_length=200, verbose_name="Tên dịch vụ")
    description = models.TextField(verbose_name="Mô tả ngắn")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Giá tiền (VNĐ)")
    image = models.ImageField(upload_to='services/', verbose_name="Hình ảnh minh họa", null=True, blank=True)
    duration = models.IntegerField(default=60, verbose_name="Thời lượng (phút)")

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.title()
        if self.description:
            # Sentence Case: Only capitalize the first letter of the string
            self.description = self.description.capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ContactInfo(models.Model):
    address = models.CharField(max_length=255, verbose_name="Địa chỉ")
    phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    email = models.EmailField(verbose_name="Email")
    facebook_name = models.CharField(max_length=100, verbose_name="Tên Facebook")
    facebook_url = models.URLField(verbose_name="Link Facebook")
    working_hours = models.CharField(max_length=255, verbose_name="Giờ mở cửa")
    qr_code = models.ImageField(upload_to='contact/', verbose_name="Mã QR thanh toán", null=True, blank=True)

    class Meta:
        verbose_name = "Thông tin liên hệ"
        verbose_name_plural = "Thông tin liên hệ"

    def __str__(self):
        return f"Liên hệ: {self.phone}"

class Booking(models.Model):
    PAYMENT_METHODS = [
        ('none', 'Chưa thanh toán'),
        ('cash', 'Tiền mặt'),
        ('transfer', 'Chuyển khoản'),
    ]
    
    customer_name = models.CharField(max_length=200, verbose_name="Tên khách hàng")
    booker_name = models.CharField(max_length=200, verbose_name="Người đặt lịch")
    services = models.ManyToManyField(Service, verbose_name="Dịch vụ")
    total_price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Tổng tiền")
    discount_percent = models.FloatField(default=0, verbose_name="Giảm giá (%)")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='none', verbose_name="PT Thanh toán")
    is_paid = models.BooleanField(default=False, verbose_name="Đã thanh toán")
    product_name = models.CharField(max_length=200, null=True, blank=True, verbose_name="Sản phẩm/Mỹ phẩm")
    product_price = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Giá sản phẩm")
    product_discount_percent = models.FloatField(default=0, verbose_name="Giảm giá sản phẩm (%)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian đặt")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Thời gian sửa")

    def __str__(self):
        return f"{self.customer_name} - {self.created_at.strftime('%H:%M %d/%m/%Y')}"

    class Meta:
        verbose_name = "Đơn đặt lịch"
        verbose_name_plural = "Danh sách đơn đặt lịch"
        ordering = ['-created_at']
