from .models import Cart

def cart_item_count(request):
    count = 0
    if request.user.is_authenticated:
        count = Cart.objects.filter(user=request.user).count()
    
    # Only return the count if it's greater than 0
    if count > 0:
        return {'cart_item_count': count}
    return {'cart_item_count': 0}
