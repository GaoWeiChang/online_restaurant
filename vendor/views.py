from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from accounts.views import check_role_restaurant
from vendor.forms import VendorForm
from vendor.models import Vendor
from django.contrib.auth.decorators import login_required, user_passes_test

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
