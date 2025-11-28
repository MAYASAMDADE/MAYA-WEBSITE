from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from django.utils.text import slugify
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# def home(request):
#     #to add images on home page
#  return render(request, 'app/home.html')

class ProductView(View):
    def get(self, request):
        studs = Product.objects.filter(category='ST')
        jhumkas = Product.objects.filter(category='JH')
        floral_earrings = Product.objects.filter(category='FL')
        geometric_earrings = Product.objects.filter(category='GE')
        return render(request, 'app/home.html', {'studs': studs, 'jhumkas': jhumkas, 'floral_earrings': floral_earrings, 'geometric_earrings':geometric_earrings})


# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()

        return render(request, 'app/productdetail.html',{'product':product, 'item_already_in_cart':item_already_in_cart})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    #print(product)          to print the id on terminal  dubug
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')



@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]

        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
            total_amount = amount + shipping_amount  # Calculate the total amount here

            return render(request, 'app/addtocart.html', {
                'carts': cart,
                'totalamount': total_amount,
                'amount': amount
            })
        else:
            return render(request, 'app/emptycart.html')


def plus_cart(request):
    if request.method =='GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        

        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount + shipping_amount
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method =='GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount


        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount': amount+ shipping_amount
        }
        return JsonResponse(data)        

@login_required
def remove_cart(request):
    if request.method =='GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'amount':amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)  


def buy_now(request):
    return render(request, 'app/buynow.html')

# def profile(request):
#  return render(request, 'app/profile.html')

# def address(request):
#     add = Customer.objects.filter(user=request.user)
#     return render(request, 'app/address.html',{'add':add, 'active': 'btn-primary'})
@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)  # Only fetch addresses for the logged-in user
    return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary'})


@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op})

# def change_password(request):
#  return render(request, 'app/changepassword.html')


# def studs(request, data=None):
#     if data is None:
#         studs = Product.objects.filter(category='ST')
#     else:
#         data = data.replace('-', ' ')  # Replace hyphens with spaces for the filter
#         if data in ['ASH Of Trend', 'Tiffany & Co.', 'Cartier', 'Silvosia']:
#             studs = Product.objects.filter(category='ST', brand=data)
#         else:
#             studs = Product.objects.filter(category='ST')  # Default to all studs if brand is invalid

#     # If no products match, make sure 'studs' is an empty list or similar.
#     if not studs:
#         studs = []

#     return render(request, 'app/studs.html', {'studs': studs})




def studs(request, data=None):
    # Initialize 'studs' as an empty queryset
    studs = Product.objects.none()

    # Define a dictionary mapping slugified brand names to actual names
    brand_map = {
        slugify('ASH Of Trend'): 'ASH Of Trend',
        slugify('Tiffany & Co.'): 'Tiffany & Co.',
        slugify('Cartier'): 'Cartier',
        slugify('Silvosia'): 'Silvosia',
    }

    if data is None:
        studs = Product.objects.filter(category='ST')
    else:
        # Get the actual brand name if it exists in the map
        brand_name = brand_map.get(data)
        if brand_name:
            studs = Product.objects.filter(category='ST', brand=brand_name)
        elif data == 'below':
            studs = Product.objects.filter(category='ST').filter(discounted_price__lt=300)
        elif data == 'above':
            studs = Product.objects.filter(category='ST').filter(discounted_price__gt=300)

    return render(request, 'app/studs.html', {'studs': studs})


def jhumkas(request, data=None):
    # Initialize 'jhumkas' as an empty queryset
    jhumkas = Product.objects.none()

    # Define a dictionary mapping slugified brand names to actual names
    brand_map = {
        slugify('ASH Of Trend'): 'ASH Of Trend',
        slugify('Tiffany & Co.'): 'Tiffany & Co.',
        slugify('Cartier'): 'Cartier',
        slugify('Silvosia'): 'Silvosia',
    }

    if data is None:
        jhumkas = Product.objects.filter(category='JH')
    else:
        # Get the actual brand name if it exists in the map
        brand_name = brand_map.get(data)
        if brand_name:
            jhumkas = Product.objects.filter(category='JH', brand=brand_name)  # Change 'studs' to 'jhumkas'
        elif data == 'below':
            jhumkas = Product.objects.filter(category='JH', discounted_price__lt=300)  # Change 'studs' to 'jhumkas'
        elif data == 'above':
            jhumkas = Product.objects.filter(category='JH', discounted_price__gt=300)  # Change 'studs' to 'jhumkas'

    return render(request, 'app/Jhumkas.html', {'jhumkas': jhumkas})



#floral_earrings
def floral_earrings(request, data=None):
    # Initialize 'jhumkas' as an empty queryset
    floral_earrings = Product.objects.none()

    # Define a dictionary mapping slugified brand names to actual names
    brand_map = {
        slugify('ASH Of Trend'): 'ASH Of Trend',
        slugify('Tiffany & Co.'): 'Tiffany & Co.',
        slugify('Cartier'): 'Cartier',
        slugify('Silvosia'): 'Silvosia',
    }

    if data is None:
        floral_earrings = Product.objects.filter(category='FL')

    else:
        # Get the actual brand name if it exists in the map
        brand_name = brand_map.get(data)
        if brand_name:
            floral_earrings = Product.objects.filter(category='FL', brand=brand_name)  # Change 'studs' to 'jhumkas'
        elif data == 'below':
            floral_earrings = Product.objects.filter(category='FL', discounted_price__lt=300)  # Change 'studs' to 'jhumkas'
        elif data == 'above':
            floral_earrings = Product.objects.filter(category='FL', discounted_price__gt=300)  # Change 'studs' to 'jhumkas'

    return render(request, 'app/floral_earrings.html', {'floral_earrings': floral_earrings})    

def geometric_earrings(request, data=None):
    # Initialize 'geometric_earrings' as an empty queryset
    geometric_earrings = Product.objects.none()

    # Define a dictionary mapping slugified brand names to actual names
    brand_map = {
        slugify('ASH Of Trend'): 'ASH Of Trend',
        slugify('Tiffany & Co.'): 'Tiffany & Co.',
        slugify('Cartier'): 'Cartier',
        slugify('Silvosia'): 'Silvosia',
    }

    if data is None:
        # Fetch all geometric earrings if no filter is applied
        geometric_earrings = Product.objects.filter(category='GE')  # Assuming 'GE' is the category for geometric earrings

    else:
        # Get the actual brand name if it exists in the map
        brand_name = brand_map.get(data)
        if brand_name:
            geometric_earrings = Product.objects.filter(category='GE', brand=brand_name)
        elif data == 'below':
            geometric_earrings = Product.objects.filter(category='GE', discounted_price__lt=300)
        elif data == 'above':
            geometric_earrings = Product.objects.filter(category='GE', discounted_price__gt=300)

    return render(request, 'app/geometric_earrings.html', {'geometric_earrings': geometric_earrings})


# def login(request):
#  return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congrats! You have successfully registered.')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})

    
@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount
    return render(request, 'app/checkout.html', {'add': add, 'totalamount': totalamount, 'cart_items': cart_items})


@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    # Handle GET request to display the profile form
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulations!! Profile Updated Successfully')
            return redirect('profile')  # Ensure you redirect to prevent re-submission
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

def search_products(request):
    query = request.GET.get('query', '').strip()
    if query:
        # Search by title (case-insensitive)
        products = Product.objects.filter(title__icontains=query)[:5]  # Limit results to 5
        results = [
            {
                "id": product.id,
                "name": product.title,  # Use 'title' instead of 'name'
                "price": product.discounted_price,  # Use 'selling_price'
                "image": product.product_image.url if product.product_image else "",  # Use 'product_image'
            }
            for product in products
        ]
    else:
        results = []  # No results for an empty query

    return JsonResponse({"products": results})