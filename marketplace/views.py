from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render

from marketplace.context_processors import get_cart_amounts, get_cart_counter
from marketplace.models import Cart
from menu.models import Category, FoodItem
from vendor.models import Vendor
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required

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
    address = request.GET['address'] # name in the input tag (name="address")
    latitude = request.GET['lat']
    longtitude = request.GET['lng']
    radius = request.GET['radius']
    keyword = request.GET['keyword']
    
    vendors = Vendor.objects.filter(vendor_name__icontains=keyword, is_approved=True, user__is_active=True) # double underscore is allow to find more specific keyword 
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count,
    }
    
    return render(request, 'marketplace/listings.html', context)