from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from marketplace.context_processors import get_cart_amounts, get_cart_counter
from marketplace.models import Cart
from menu.models import Category, FoodItem
from vendor.models import Vendor
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D  # ``D`` is a shortcut for ``Distance``
from django.contrib.gis.db.models.functions import Distance

def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8] # [:8] = get 8 restaurants
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count,
    }
    return render(request, 'marketplace/listings.html', context)

def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    # use prefetch_related when we want the instance from another class that connected foreign key
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset=FoodItem.objects.filter(is_available=True)
        )
    )
    
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/vendor_detail.html', context)

def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        # check AJAX request
        if(request.headers.get('x-requested-with') == 'XMLHttpRequest'):
            # check if the food exist
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # check user is already added to the cart
                try:
                    checkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    checkCart.quantity += 1
                    checkCart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Increased quantity', 'cart_counter': get_cart_counter(request), 'qty': checkCart.quantity, 'cart_amount': get_cart_amounts(request)}) # get_cart_counter to show total fooditem in cart
                except:
                    checkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'Added food to the cart', 'cart_counter': get_cart_counter(request), 'qty': checkCart.quantity, 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})
    
def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        # check AJAX request
        if(request.headers.get('x-requested-with') == 'XMLHttpRequest'):
            # check if the food exist
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # check user is already added to the cart
                try:
                    checkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    if checkCart.quantity > 1:
                        checkCart.quantity -= 1
                        checkCart.save()
                    else:
                        checkCart.delete()
                        checkCart.quantity = 0
                    return JsonResponse({'status': 'Success', 'cart_counter': get_cart_counter(request), 'qty': checkCart.quantity, 'cart_amount': get_cart_amounts(request)}) # get_cart_counter to show total fooditem in cart
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your cart'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})

@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/cart.html', context)

def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if(request.headers.get('x-requested-with') == 'XMLHttpRequest'):
            try:
                # check if cart exists
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'Success', 'message': 'Cart item has been deleted!','cart_counter': get_cart_counter(request),  'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'Cart item does not exist!'})
    else:
        return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
    
def search(request):
    if 'address' not in request.GET:
        return redirect('marketplace')
    else:
        address = request.GET['address'] # name in the input tag (name="address")
        latitude = request.GET['lat']
        longtitude = request.GET['lng']
        radius = request.GET['radius']
        keyword = request.GET['keyword']
    
    # get food name
    fetch_vendor_by_fooditem = FoodItem.objects.filter(food_title__icontains=keyword, is_available=True).values_list('vendor', flat=True) # ดึงข้อมูลเฉพาะคอลัมน์ 'vendor' ออกมาเป็นลิสต์แบบเรียบ (flat list)
    
    # ใช้ Q เพื่อสร้างเงื่อนไขการค้นหาที่ซับซ้อนและยืดหยุ่น โดยเฉพาะเมื่อต้องการใช้ operator ทางตรรกศาสตร์ (logical operators) เช่น OR (|) หรือ AND (&)
    vendors = Vendor.objects.filter(Q(id__in=fetch_vendor_by_fooditem) | Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True))
    if latitude and longtitude and radius:
        # Distances will be calculated from this point, which does not have to be projected.
        pnt = GEOSGeometry('POINT(%s %s)' %(longtitude, latitude))
        vendors = Vendor.objects.filter(Q(id__in=fetch_vendor_by_fooditem) | Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True), 
                                        user_profile__location__distance_lte=(pnt, D(km=radius))
                                        ).annotate(distance=Distance('user_profile__location', pnt)).order_by('distance')
        for v in vendors:
            v.kms = round(v.distance.km, 1)
        
    vendor_count = vendors.count()
    
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count,
        'source_location': address,
    }
    
    return render(request, 'marketplace/listings.html', context)