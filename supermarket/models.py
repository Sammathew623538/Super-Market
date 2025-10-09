from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta



class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images', null=True, blank=True) 

    def __str__(self):
        return str(self.user.username)
    


    

class Category(models.Model):
 name=models.CharField(max_length=100)
 image=models.ImageField(upload_to='cat')
 slug = models.SlugField(unique=True)
 def __str__(self):
   return self.name
def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)



class Product(models.Model):
  name=models.CharField(max_length=100)

  slug = models.SlugField( blank=True,unique=True) 
  category=models.ForeignKey(Category,on_delete=models.CASCADE)
  image=models.ImageField(upload_to='product')
  description=models.TextField(max_length=200,blank=True)



  # Pricing
  mrp = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

  discount = models.IntegerField(default=0)  # % discount

    # Stock & Quantity
  qty = models.CharField(max_length=50, default="1 unit")  # Example: "250 ml", "1 kg"
  stock = models.PositiveIntegerField(default=0)

    # Extra details
  rating = models.FloatField(default=4.0)
  reviews = models.IntegerField(default=0)  # Eg: 934 reviews
  delivery_time = models.CharField(max_length=50, default="10 mins")  # Zepto style
    

  def final_price(self):
        """Calculate discounted price"""
        if self.discount > 0:
            return round(self.mrp - (self.mrp * self.discount / 100), 2)
        return self.mrp
  
  def save(self, *args, **kwargs):
        if not self.slug:  # Automatically slug generate cheyyum
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
  def __str__(self):
    return self.name
  




class Cart(models.Model):   # Capital C
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"

    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    def total_price(self):
        return sum(item.subtotal() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")  # Capital C
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    def subtotal(self):
        return self.product.final_price() * self.quantity

    class Meta:
        unique_together = ("cart", "product")  # same product repeat avoid




class Buy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    address = models.TextField()
    Email=models.EmailField(null=True)
    phone_number = models.CharField(max_length=15)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity
        if not self.delivery_date:
            self.delivery_date = timezone.now() + timedelta(minutes=30)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"