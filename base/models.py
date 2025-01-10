from django.db import models
from users.models import EmailUser
from django.core.validators import MinValueValidator

# Create your models here.

class CompanyUser(models.Model):
   user = models.OneToOneField(EmailUser , on_delete=models.CASCADE)
   
   gstin = models.CharField(max_length=15 , unique=True , null=True , blank=False)
   brand_name = models.CharField(max_length=200 , null=True , blank=False)
   phone = models.CharField(max_length=10 , unique=True , null=True , blank=False)
   address = models.TextField(null=True , blank=True)

   is_approved = models.BooleanField(default=False)
   is_archived = models.BooleanField(default=False)

   created = models.DateTimeField(auto_now_add=True) 

   def __str__(self):
      return f"{self.user.email.split('@')[0]}-{self.brand_name}"
   

class Product(models.Model):
   image = models.URLField(null=True , blank=True)
   name = models.CharField(max_length=200 , null=True , blank=True)
   description = models.TextField(max_length=200 , null=True , blank=True)
   price = models.DecimalField(max_digits=10 , decimal_places=2 , validators=[MinValueValidator(0)] ,default=0.00)

   in_stock = models.BooleanField(default=True) 

   created = models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return f"{self.name}-{self.price}"

class CartItem(models.Model):
   user = models.ForeignKey(EmailUser , on_delete=models.SET_NULL , null=True)
   product = models.ForeignKey(Product , on_delete=models.SET_NULL , null=True)
   quantity = models.IntegerField(default=0,validators=[MinValueValidator(0)])
   total_amount = models.DecimalField(max_digits=10 , decimal_places=2 , validators=[MinValueValidator(0)] , default=0.00)

   created = models.DateTimeField(auto_now_add=True)   

class Cart(models.Model):
   user = models.ForeignKey(EmailUser , on_delete=models.CASCADE)
   brand = models.ForeignKey(CompanyUser , on_delete=models.CASCADE)
   items = models.ManyToManyField(CartItem , blank=True)
   cart_total = models.DecimalField(max_digits=10 , decimal_places=2 , validators=[MinValueValidator(0)] ,default=0.00)
   cart_quantity = models.IntegerField(default=0)

   is_active=models.BooleanField(default=True)
   ordered = models.BooleanField(default=False)

   created = models.DateTimeField(auto_now_add=True)