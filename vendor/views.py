from django.shortcuts import render

def restaurant_profile(request):
    return render(request, 'restaurant/restaurant_profile.html')
