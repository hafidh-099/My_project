from django.db import models

# Create your models here.

# Food Item Model
class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    img_url = models.CharField(max_length=3000, null=True,blank=True)

    def __str__(self):
        return f"{self.name}"

# Customer Model
class Customer(models.Model):
    name = models.CharField(max_length=50 ,null=False,blank=False)
    phone = models.CharField(max_length=15,null=False,blank=False,unique=True)
    address = models.CharField(max_length=100,null=False,blank=False)
    password = models.CharField(max_length=100,default='')

    def __str__(self):
        return f"{self.name}"

# Order Model
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    food_items = models.ManyToManyField(FoodItem)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order from {self.id} - {self.customer.name}"
