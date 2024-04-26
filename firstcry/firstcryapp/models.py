import datetime
import os
from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser,BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.utils.html import mark_safe


class NonDeleted(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = False)
    
class SoftDelete(models.Model):
    is_deleted = models.BooleanField(default=False)
    everything = models.Manager()
    objects = NonDeleted()

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
   

    class Meta:
        abstract = True

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username=None
    email = models.EmailField(unique=True)
    ban_status = models.BooleanField(default=False)
    mobile = models.BigIntegerField(null=True)

    USERNAME_FIELD ='email'
    REQUIRED_FIELDS=[]
    objects = UserManager()

    def __str__(self):
        return self.email
    
# Add Category --------------------------------------------------
visibility_choices = [
    ('1','public'),
    ('2','hidden')
]
type_choices = [
    ('shirt','1'),
    ('pants','2'),
    ('t-shirt','3'),
    ('both','4'),
]
class categories(SoftDelete):
    titile = models.CharField(max_length=100)
    description = models.CharField(max_length=800)
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)
    visibility = models.CharField( max_length = 20, choices = visibility_choices, 
        default = 'public'
        )
    type = models.CharField( max_length = 10,choices = type_choices, default = '1')
    gender = models.CharField( max_length = 20,null=True,blank=True )
   
class color(models.Model): 
    name = models.CharField(max_length = 500)
    code = models.CharField(max_length = 100)


class variation(models.Model):
    colors = models.ForeignKey(color,on_delete = models.DO_NOTHING,null=True)
    zerotothreeM = models.BigIntegerField(default = 0,null=True)
    threetosixM = models.BigIntegerField(default = 0,null=True)
    sixtonineM = models.BigIntegerField(default = 0,null=True)
    ninetotwelveM = models.BigIntegerField(default = 0,null=True)
    twelvetoeighteenM = models.BigIntegerField(default = 0,null=True)
    eighteentotwentyfourM = models.BigIntegerField(default = 0,null=True)
    twotofourY = models.BigIntegerField(default = 0,null=True)
    fourtosixY = models.BigIntegerField(default = 0,null=True)
    sixtoeightY = models.BigIntegerField(default = 0,null=True)
    total = models.BigIntegerField(default = 0,null=True)
    

class brands(models.Model):
    name = models.CharField(max_length = 1000)
    description = models.CharField(max_length=5000)
    specs = models.CharField(max_length=5000,null=True, blank=True)
    logo = models.ImageField(upload_to='com_logo',null=True, blank=True)

# products-----------------------------



class products(SoftDelete):
    category = models.ForeignKey(categories, on_delete=models.CASCADE)
    varient = models.ForeignKey(variation,on_delete = models.DO_NOTHING,null = True)
    name = models.CharField(max_length=5000)
    brand = models.ForeignKey(brands,on_delete=models.DO_NOTHING,null=True,blank=True)
    image = models.ImageField(upload_to='prod_image', null=True, blank=True)
    description = models.CharField(max_length=1000,null=True)
    necktype = models.CharField(max_length=50,null = True)
    sleevetype = models.CharField(max_length=50,null = True)
    length = models.CharField(max_length = 100,null = True)
    waist = models.CharField(max_length=100,blank = True,null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2,null=True)
    deal= models.IntegerField(null=True,blank=True)
    Offer_price = models.DecimalField(max_digits=6, decimal_places=2,null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
 


# whishlist -----------------------------------

class whishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(products,on_delete=models.CASCADE)
    size = models.CharField( max_length = 50,null=True,blank=True )
    date = models.DateTimeField(auto_now_add=True,blank=True)


# cart ------------------------------------------------

class cart(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(products,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True ,blank=True)
    size = models.CharField( max_length = 50,null=True,blank=True )
    quantity = models.IntegerField(default=1)

order_status_choices = [
    ('1','Pending'),
    ('2','Processed'),
    ('3','Shipped'),
    ('4','Delivered'),
    ('5','Cancelled'),
    ('6','Returned'),
    ('7', 'Cancelled by Admin')
]

class coupon(models.Model):
    name = models.CharField(max_length=10,null=True,blank=True)
    description = models.CharField(max_length=200,null=True,blank=True)
    discount = models.IntegerField(default=0)
    min_amount = models.IntegerField(default=0)
    start_date = models.DateField(blank=True,null=True)
    end_date = models.DateField(null=True,blank=True)

# Address------------------------------------
class address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    house_name = models.CharField(max_length=500)
    street_name = models.CharField(max_length=1000)
    landmark = models.CharField(max_length=500,null=True,blank=True)
    pincode = models.BigIntegerField()
    city = models.CharField(max_length=500)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=100,default='India')
    mobile = models.BigIntegerField(default=0)
    default_value = models.BooleanField(default=False)

#order ---------------------------------------------------
class order(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    user_name = models.CharField(max_length = 500,null=True,blank=True)
    user_housename = models.CharField(max_length = 500,null=True,blank=True)
    user_street = models.CharField(max_length = 500,null=True,blank=True)
    user_landmark = models.CharField(max_length=500,null=True,blank=True)
    user_pincode = models.BigIntegerField(null=True,blank=True)
    user_city = models.CharField(max_length=500,null=True,blank=True)
    user_state = models.CharField(max_length=200,null=True,blank=True)
    user_country = models.CharField(max_length=100,default='India')
    user_mobile = models.BigIntegerField(default=0)
    order_status = models.CharField(max_length=50,choices=order_status_choices,default='Pending')
    date = models.DateTimeField(auto_now_add=True ,blank=True)
    total_amount = models.DecimalField(max_digits=6, decimal_places=2,null=True)
    payment_method = models.CharField(max_length=500,null=True,blank=True)
    payment_id =models.CharField(max_length=500,null=True,blank=True)
    coupon = models.ForeignKey(coupon,on_delete=models.DO_NOTHING,null=True,blank=True)

class order_items(models.Model):
    order = models.ForeignKey(order,on_delete = models.DO_NOTHING)
    product = models.ForeignKey(products,on_delete=models.CASCADE)
    size = models.CharField(max_length=100,null=True,blank=True)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2,null=True)
    deal= models.IntegerField(null=True,blank=True)
    Offer_price = models.DecimalField(max_digits=6, decimal_places=2,null=True)
    total = models.DecimalField(max_digits=6, decimal_places=2,null=True)

return_status_choices = [
    ('1','Returned'),
    ('2','Cancelled'),
    ('3','Cancelled by Admin')
]

class return_order(models.Model):
    order = models.ForeignKey(order,on_delete=models.DO_NOTHING)
    user =models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    reason = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True ,blank=True)
    status = models.CharField(max_length=50,choices=return_status_choices,default='Returned')
    stock_status = models.BooleanField(default=False)
    

# class return_product(models.Model):
#     return_order = models.ForeignKey(return_order,on_delete=models.DO_NOTHING ,default=2)
#     order = models.ForeignKey(order,on_delete=models.DO_NOTHING)
#     product = models.ForeignKey(products,on_delete=models.CASCADE,default=31)
#     size = models.CharField(max_length=100,null=True,blank=True)
#     quantity = models.IntegerField(default=0)
#     stock_status = models.BooleanField(default=False)




 






    
















# Testing --------------------------------------------------------------
class testimage(models.Model):
    titile = models.CharField(max_length=100)
    description = models.CharField(max_length=800)
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)



class CroppedImage(models.Model):
    file = models.ImageField(upload_to='images123')
    uploaded = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=500,null=True,blank=True)

    def __str__(self):
        return str(self.pk)