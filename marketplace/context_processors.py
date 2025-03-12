from marketplace.models import Cart


def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items:
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
            else:
                cart_count = 0
        except:
            cart_count = 0
    
    ''' return type
        {"cart_count": 5}  # กรณีมีสินค้าในตะกร้ารวม 5 ชิ้น
        {"cart_count": 0}  # กรณีไม่มีสินค้าในตะกร้า
    '''
    return dict(cart_count=cart_count)
