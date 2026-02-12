from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Category, Service, ContactInfo, Booking
from django import forms
from django.contrib.auth.decorators import login_required
import json

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['category', 'name', 'description', 'price', 'image', 'duration']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ['address', 'phone', 'email', 'facebook_name', 'facebook_url', 'working_hours', 'qr_code']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'facebook_name': forms.TextInput(attrs={'class': 'form-control'}),
            'facebook_url': forms.URLInput(attrs={'class': 'form-control'}),
            'working_hours': forms.TextInput(attrs={'class': 'form-control'}),
            'qr_code': forms.FileInput(attrs={'class': 'form-control'}),
        }

def index(request):
    categories = Category.objects.all().prefetch_related('services')
    contact = ContactInfo.objects.last()
    return render(request, 'spa_app/index.html', {
        'categories': categories,
        'contact': contact
    })

def confirm_booking(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            service_ids = data.get('service_ids', [])
            product_name = data.get('product_name', '').strip()
            product_price = float(data.get('product_price', 0))
            
            if not service_ids and not product_name:
                return JsonResponse({'status': 'error', 'message': 'Chưa chọn dịch vụ hoặc sản phẩm'})
                
            services = Service.objects.filter(id__in=service_ids)
            
            # Calculate costs and duration
            # Convert to float to avoid Decimal * float error
            total_price = float(sum(s.price for s in services)) if services else 0.0
            total_duration = sum(s.duration for s in services) if services else 0
            service_names = ", ".join([s.name for s in services]) if services else "Mua lẻ sản phẩm"
            
            discount_percent = float(data.get('discount_percent', 0))
            product_discount_percent = float(data.get('product_discount_percent', 0))
            
            discount_amount = total_price * (discount_percent / 100)
            product_discount_amount = product_price * (product_discount_percent / 100)
            
            final_total = (total_price - discount_amount) + (product_price - product_discount_amount)
            
            from datetime import datetime
            now = datetime.now()
            
            # Create Booking record (initially unpaid)
            booking = Booking.objects.create(
                customer_name=data.get('customer_name', 'Ẩn danh'),
                booker_name=data.get('booker_name', 'Ẩn danh'),
                total_price=final_total,
                discount_percent=discount_percent,
                product_name=product_name,
                product_price=product_price,
                product_discount_percent=product_discount_percent,
                payment_method='none',
                is_paid=False
            )
            booking.services.set(services)
            
            # Mock invoice data
            invoice = {
                'id': f"SPA{now.year}-{booking.id:04d}",
                'booking_id': booking.id,
                'booker_name': booking.booker_name,
                'customer_name': booking.customer_name,
                'date': now.strftime("%d/%m/%Y"),
                'service_names': service_names,
                'duration': f"{total_duration} phút",
                'price': f"{total_price:,.0f} VNĐ",
                'discount_percent': discount_percent,
                'discount_amount': f"{discount_amount:,.0f} VNĐ",
                'product_name': product_name,
                'product_price': f"{product_price:,.0f} VNĐ",
                'product_discount_percent': product_discount_percent,
                'product_discount_amount': f"{product_discount_amount:,.0f} VNĐ",
                'total': f"{final_total:,.0f} VNĐ",
                'services': [{'name': s.name, 'price': f"{s.price:,.0f} VNĐ"} for s in services]
            }
            
            return JsonResponse({'status': 'success', 'invoice': invoice})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def finalize_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            booking_id = data.get('booking_id')
            method = data.get('method') # 'cash' or 'transfer'
            
            booking = get_object_or_404(Booking, id=booking_id)
            booking.payment_method = method
            booking.is_paid = True
            booking.save()
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

# Management Views
@login_required
def manage_services(request):
    services = Service.objects.all().order_by('category')
    contacts = ContactInfo.objects.all()
    return render(request, 'spa_app/manage.html', {
        'services': services,
        'contacts': contacts
    })

@login_required
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_services')
    else:
        form = ServiceForm()
    return render(request, 'spa_app/service_form.html', {'form': form, 'title': 'Thêm dịch vụ mới'})

@login_required
def edit_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('manage_services')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'spa_app/service_form.html', {'form': form, 'title': 'Chỉnh sửa dịch vụ'})

@login_required
def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        return redirect('manage_services')
    return render(request, 'spa_app/service_confirm_delete.html', {'service': service})

# Contact Management
@login_required
def edit_contact(request, pk):
    contact = get_object_or_404(ContactInfo, pk=pk)
    if request.method == 'POST':
        form = ContactInfoForm(request.POST, request.FILES, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('manage_services')
    else:
        form = ContactInfoForm(instance=contact)
    return render(request, 'spa_app/service_form.html', {'form': form, 'title': 'Chỉnh sửa thông tin liên hệ'})

@login_required
def add_contact(request):
    if request.method == 'POST':
        form = ContactInfoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_services')
    else:
        form = ContactInfoForm()
    return render(request, 'spa_app/service_form.html', {'form': form, 'title': 'Thêm thông tin liên hệ'})

@login_required
def delete_contact(request, pk):
    contact = get_object_or_404(ContactInfo, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect('manage_services')
    return render(request, 'spa_app/service_confirm_delete.html', {'contact': contact, 'is_contact': True})

@login_required
def booking_history(request):
    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'spa_app/manage_history.html', {'bookings': bookings})

@login_required
def edit_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    all_services = Service.objects.all().order_by('category__name', 'name')
    categories = Category.objects.all().prefetch_related('services')
    
    if request.method == 'POST':
        # Update text fields
        booking.customer_name = request.POST.get('customer_name')
        booking.booker_name = request.POST.get('booker_name')
        booking.product_name = request.POST.get('product_name')
        
        # Numeric fields with defaults
        product_price = float(request.POST.get('product_price') or 0)
        discount_percent = float(request.POST.get('discount_percent') or 0)
        product_discount_percent = float(request.POST.get('product_discount_percent') or 0)
        
        booking.product_price = product_price
        booking.discount_percent = discount_percent
        booking.product_discount_percent = product_discount_percent
        booking.is_paid = 'is_paid' in request.POST
        
        # Update Services (ManyToMany)
        service_ids = request.POST.getlist('service_ids')
        selected_services = Service.objects.filter(id__in=service_ids)
        booking.services.set(selected_services)
        
        # Calculate new total based on CURRENT service prices
        base_price = float(sum(s.price for s in selected_services))
        discount_amount = base_price * (discount_percent / 100)
        product_discount_amount = product_price * (product_discount_percent / 100)
        booking.total_price = (base_price - discount_amount) + (product_price - product_discount_amount)
        
        # Adjust payment method based on status
        if booking.is_paid and booking.payment_method == 'none':
            booking.payment_method = 'cash' 
        elif not booking.is_paid:
            booking.payment_method = 'none'
            
        from django.utils import timezone
        booking.updated_at = timezone.now()
        booking.save()
        return redirect('booking_history')
    
    # Get initial selected service IDs for the JS logic
    selected_service_ids = list(booking.services.values_list('id', flat=True))
    
    return render(request, 'spa_app/booking_edit_form.html', {
        'booking': booking,
        'all_services': all_services,
        'categories': categories,
        'selected_service_ids': selected_service_ids
    })

@login_required
def delete_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        booking.delete()
        return redirect('booking_history')
    return render(request, 'spa_app/booking_confirm_delete.html', {'booking': booking})

@login_required
def clear_booking_history(request):
    if request.method == 'POST':
        Booking.objects.all().delete()
        return redirect('booking_history')
    return render(request, 'spa_app/clear_history_confirm.html')
