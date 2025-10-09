from django.shortcuts import render
from.models import Category,Product
from.forms import  CategoryForm,ProductForm,ProfileForm, RegisterForm
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect
from.models import profile
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Product
from .models import Buy
from .forms import BuyForm
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test

from django.contrib.admin.views.decorators import staff_member_required





def god(request):
    return render(request,'start.html')

def home(request):
    categories = Category.objects.all()
    category_products = {}

    for category in categories:
        # ithil 5 products mathram
        products = Product.objects.filter(category=category)[:4]
        category_products[category] = products

    return render(request, "main.html", {
        "categories": categories,
        "category_products": category_products
    })



def search_products(request):
    query = request.GET.get("q", "").strip()
    results = Product.objects.none()

    if query:
        results = Product.objects.filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query)   # if category is ForeignKey with 'name' field
        )

    return render(request, "search.html", {"query": query, "results": results})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    recommendations = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:8]  
    return render(request, "product_detail.html", {"product": product, "recommendations": recommendations})





def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)   # Category fetch
    products = Product.objects.filter(category=category) [:14] # Related products fetch

    return render(request, "category_products.html", {
        "category": category,
        "products": products,
    })




def product_details(request, slug):
    product = get_object_or_404(Product, slug=slug)
    recommendations = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:12]  
    return render(request, "product_details.html", {"product": product,  "recommendations": recommendations,})


def loginpage(request):
    error_message = None 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            print("user authenticated")
            return redirect(home)
        else:
              error_message = "Invalid username or password."
    return render(request, 'login.html',{'error_message': error_message})



def logoutpage(request):
    logout(request)
    return redirect(loginpage)


def profilepage(request):
    usr = request.user
    pro= profile.objects.get(user=usr)
    return render(request, 'profile.html', {'pro': pro})  






def proedit(request,):
    pro=profile.objects.get(user=request.user)
    if request.method =="POST":
        form = ProfileForm(request.POST, request.FILES, instance=pro)
        if form.is_valid():
           form.save()
           return redirect(profilepage)
    else:
        form=ProfileForm(instance=pro)        
    return render(request,'edit_profile.html',{'form':form})







def Register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect(loginpage)
          
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})








@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()

    return redirect("view_cart")


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, "cart.html", {"cart": cart})


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect("view_cart")





@login_required
def buy_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        form = BuyForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.product = product
            order.save()
            return render(request, "buy_success.html", {"order": order})
    else:
        form = BuyForm()

    return render(request, "buy_form.html", {"form": form, "product": product})







@login_required
def buy_products(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        form = BuyForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.product = product
            order.total_price = product.price * order.quantity
            order.save()

            # Email send
            recipient_email = order.Email or request.user.email
            if recipient_email:
                send_mail(
                    subject=f"Order Confirmation - {order.product.name}",
                    message=f"Hello {order.user.first_name or order.user.username},\n\n"
                            f"Thank you for your order.\n\n"
                            f"Order Details:\n"
                            f"Product: {order.product.name}\n"
                            f"Quantity: {order.quantity}\n"
                            f"Total Price: ₹{order.total_price}\n"
                            f"Delivery Address: {order.address}\n"
                            f"Phone: {order.phone_number}\n"
                            f"Order Date: {order.order_date}\n\n"
                            "We will notify you once your order is shipped.\n\n"
                            "Best regards,\n"
                            "PetCare Team",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[recipient_email],
                    fail_silently=False
                )

            # Redirect to a success page
            return render(request, "buy_success.html", {"order": order})
    else:
        form = BuyForm()

    return render(request, "buy_form.html", {"form": form, "product": product})






@staff_member_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = ProductForm()
    return render(request, "add_product.html", {"form": form})






# only superuser check
def superuser_required(view_func):
    decorated_view_func = user_passes_test(
        lambda u: u.is_superuser
    )(view_func)
    return decorated_view_func

@superuser_required
def user_list(request):
    users = User.objects.all()
    return render(request, "user_list.html", {"users": users})

@superuser_required
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user.is_superuser:   # prevent superuser deleting other superusers
        return redirect("user_list")
    user.delete()
    return redirect("user_list")




