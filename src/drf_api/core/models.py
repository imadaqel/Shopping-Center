from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user

class Item(models.Model):
    CATEGORY=(
        ('Shirts','Shirts'),
        ('Shoes','Shoes'),
        ('Trousers','Trousers'),
        ('Dress','Dress')
    )
    
    itemName=models.CharField(max_length=70,null=True)
    details=models.CharField(max_length=200,null=True)
    price=models.FloatField(null=True)
    image=models.ImageField()
    quantity=models.CharField(max_length=200,null=True)
    category = models.CharField(choices=CATEGORY, max_length=20)
    entry_date=models.DateTimeField(auto_now_add=True,null=True)
    # slug = models.SlugField()
    
    def __str__(self):
        return self.itemName

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            "pk" : self.pk
        
        })

    def get_add_to_cart_url(self) :
        return reverse("core:add-to-cart", kwargs={
            "pk" : self.pk
        })

    def get_remove_from_cart_url(self) :
        return reverse("core:remove-from-cart", kwargs={
            "pk" : self.pk
        })

class OrderItem(models.Model) :
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


    def __str__(self):
        return f"{self.quantity} of {self.item}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_discount_item_price()
        return self.get_total_item_price()    



class Order(models.Model):
    STATUS=(
        ('Pending','Pending'),
        ('Deleviered','Deleviered'),
        ('in progress','in progress'),
        ('out of order','out of order')
    )
    user=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.SET_NULL)
    item=models.ManyToManyField(OrderItem,null=True)

    quantity=models.CharField(max_length=70,null=True)
    status=models.CharField(max_length=200,choices=STATUS)
    price=models.FloatField(null=True)
    image=models.CharField(max_length=200,null=True)
    quantity=models.CharField(max_length=200,null=True)
    entry_date=models.DateTimeField(auto_now_add=True,null=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user
    

    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

class CheckoutAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user

class Payment(models.Model):
    stripe_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
