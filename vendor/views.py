from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from accounts.views import check_role_restaurant
from menu.forms import CategoryForm, FoodItemForm
from menu.models import Category, FoodItem
from orders.models import Order, OrderedFood
from vendor.forms import OpeningHourForm, VendorForm
from vendor.models import OpeningHour, Vendor
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.defaultfilters import slugify

def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor

# adding decorator because we want logged in user only due to request.user information
@login_required(login_url='login')
@user_passes_test(check_role_restaurant)
def restaurant_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)
    
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Setting updated.')
            return redirect('restaurant_profile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)
        
    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor
    }
    return render(request, 'restaurant/restaurant_profile.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_restaurant)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at') # order by attribute "created_at"
    context = {
        'categories': categories
    }
    return render(request, 'restaurant/menu_builder.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_restaurant)
def fooditems_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor, category=category)

    context = {
        'fooditems': fooditems,
        'category': category,
    }
        
    return render(request, 'restaurant/fooditems_by_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_restaurant)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request) # vendor
            
            category.save() # here the category_id will generated
            category.slug = slugify(category_name)+'-'+str(category.id) # (slug-categoryId) this will make slug unique
            category.save()
            messages.success(request, 'Category added successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'restaurant/add_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_restaurant)
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request) # vendor
            category.slug = slugify(category_name) # slug
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'restaurant/edit_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_restaurant)
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category has been deleted successfully')
    return redirect('menu_builder')

@login_required(login_url='login')
@user_passes_test(check_role_restaurant)
def add_food(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES) # use "request.FILES" when only file type in form
        if form.is_valid():
            foodtitle = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request) # vendor
            food.slug = slugify(foodtitle) # slug
            form.save()
            messages.success(request, 'Menu added successfully!')
            return redirect('fooditems_by_category', food.category.id)
        else:
            print(form.errors)
    else:
        form = FoodItemForm()
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request)) # choose only category belongs to vendor
    context = {
        'form': form,
    }
    return render(request, 'restaurant/add_food.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_restaurant)
def edit_food(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            foodtitle = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request) # vendor
            food.slug = slugify(foodtitle) # slug
            form.save()
            messages.success(request, 'Menu updated successfully!')
            return redirect('fooditems_by_category', food.category.id)
        else:
            print(form.errors)
    else:
        form = FoodItemForm(instance=food)
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request)) # choose only category belongs to vendor
    context = {
        'form': form,
        'food': food,
    }
    return render(request, 'restaurant/edit_food.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_restaurant)
def delete_food(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    food.delete()
    messages.success(request, 'The Menu has been deleted successfully')
    return redirect('fooditems_by_category', food.category.id)


def opening_hours(request):
    opening_hours = OpeningHour.objects.filter(vendor=get_vendor(request))
    form = OpeningHourForm()
    context = {
        'form': form,
        'opening_hours': opening_hours,
    }
    return render(request, 'restaurant/opening_hours.html', context)

def add_opening_hours(request):
    if request.user.is_authenticated:
        # request.headers.get('x-requested-with') == 'XMLHttpRequest' ใช้เพื่อตรวจสอบว่าคำขอ (request) ที่ส่งมานั้นเป็น AJAX request หรือไม่
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
            day = request.POST.get('day')
            from_hour = request.POST.get('from_hour')
            to_hour = request.POST.get('to_hour')
            is_closed = request.POST.get('is_closed')
            
            try:
                hour = OpeningHour.objects.create(vendor=get_vendor(request), day=day, from_hour=from_hour, to_hour=to_hour, is_closed=is_closed) # สร้างข้อมูลใหม่ในฐานข้อมูล
                if hour:
                    day = OpeningHour.objects.get(id=hour.id)
                    if day.is_closed:
                        response = {'status':'success', 'id': hour.id, 'day': day.get_day_display(), 'is_closed':'Closed'}
                    else:
                        response = {'status':'success', 'id': hour.id, 'day': day.get_day_display(), 'from_hour': hour.from_hour, 'to_hour': hour.to_hour}
                return JsonResponse(response)
            except IntegrityError as e: # ถ้ามีข้อผิดพลาดจากการเพิ่มข้อมูลลงในฐานข้อมูล
                response = {'status':'failed', 'message': 'Opening hour ('+ from_hour + ' - ' + to_hour +') already exists'} # สร้างข้อความแจ้งเตือนว่าข้อมูลที่ต้องการเพิ่มนั้นมีอยู่แล้ว
                return JsonResponse(response) 
        else:
            return HttpResponse('Invalid Request')
        
def remove_opening_hours(request, pk=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            hour = get_object_or_404(OpeningHour, pk=pk)
            hour.delete()
            return JsonResponse({'status':'success', 'id': pk})
        
def order_detail(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order, fooditem__vendor=get_vendor(request))
        context = {
            'order': order,
            'ordered_food': ordered_food,
            'subtotal': order.get_total_by_vendor()['subtotal'],
            'tax_data': order.get_total_by_vendor()['tax_dict'],
            'grand_total': order.get_total_by_vendor()['grand_total'],
        }
    except:
        return redirect('vendor')
    return render(request, 'restaurant/order_detail.html', context)

def my_orders(request):
    vendor = Vendor.objects.get(user=request.user)
    orders = Order.objects.filter(vendors__in=[vendor.id], is_ordered=True).order_by('-created_at') 

    context = {
        'orders': orders,
    }
    return render(request, 'restaurant/my_orders.html', context)
