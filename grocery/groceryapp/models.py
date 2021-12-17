from django.db import models
#from .models import Category,QuantityVariant
from django.contrib.auth.models import (
    AbstractUser,)
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


#
#from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from .utils import unique_otp_generator
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save

import random
import os
import requests

# class UserManager(BaseUserManager):
#     def create_user(self, phone, password=None, is_staff=False, is_active=True, is_admin=False):
#         if not phone:
#             raise ValueError('users must have a phone number')
#         if not password:
#             raise ValueError('user must have a password')

#         user_obj = self.model(
#             phone=phone
#         )
#         user_obj.set_password(password)
#         user_obj.staff = is_staff
#         user_obj.admin = is_admin
#         user_obj.active = is_active
#         user_obj.save(using=self._db)
#         return user_obj

#     def create_staffuser(self, phone, password=None):
#         user = self.create_user(
#             phone,
#             password=password,
#             is_staff=True,


#         )
#         return user

#     def create_superuser(self, phone, password=None):
#         user = self.create_user(
#             phone,
#             password=password,
#             is_staff=True,
#             is_admin=True,


#         )
#         return user


class User(AbstractUser):
    #id = models.AutoField(primary_key=True)
    phone_regex = RegexValidator( regex   =r'^\+?1?\d{9,14}$', message ="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone       = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    username    = None
    name        = models.CharField(max_length=20 )
    staff       = models.BooleanField(default=False)
    email       = models.EmailField(verbose_name='email address', max_length=255,unique=True)
    is_admin   = models.BooleanField('is_admin',default=False)
    is_deliveryboy    = models.BooleanField('is_deliveryboy',default=False)
    is_customer = models.BooleanField('Is customer',default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
# def upload_image_path_profile(instance, filename):
#     new_filename = random.randint(1,9996666666)
#     name, ext = get_filename_ext(filename)
#     final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
#     return "profile/{new_filename}/{final_filename}".format(
#             new_filename=new_filename,
#             final_filename=final_filename
#     )
         

# def get_filename_ext(filepath):
#     base_name = os.path.basename(filepath)
#     name, ext = os.path.splitext(base_name)
#     return name, ext


# class Profile(models.Model):
#     user            =   models.OneToOneField(User, on_delete= models.CASCADE)
#     email           =   models.EmailField( blank = True, null = True)
#     image           =   models.ImageField(upload_to = upload_image_path_profile, default=None, null = True, blank = True)
#     address         =   models.CharField(max_length = 900, blank = True, null = True)
#     city            =   models.CharField(max_length = 30, blank = True, null = True)
#     first_count     =   models.IntegerField(default=0, help_text='It is 0, if the user is totally new and 1 if the user has saved his standard once' )

#     def __str__(self):
#         return str(self.user) 




# def user_created_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         Profile.objects.get_or_create(user = instance)
# post_save.connect(user_created_receiver, sender = User)



class PhoneOTP(models.Model):
    phone_regex = RegexValidator( regex   =r'^\+?1?\d{9,14}$', message ="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone       = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    otp         = models.CharField(max_length = 9, blank = True, null= True)
    count       = models.IntegerField(default = 0, help_text = 'Number of otp sent')
    logged      = models.BooleanField(default = False, help_text = 'If otp verification got successful')
    forgot      = models.BooleanField(default = False, help_text = 'only true for forgot password')
    forgot_logged = models.BooleanField(default = False, help_text = 'Only true if validdate otp forgot get successful')


    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)





# class User(AbstractUser):
#     is_admin=models.BooleanField('Is admin',default=False)
#     is_customer=models.BooleanField('Is customer',default=False)
#     phno=models.BigIntegerField()
    #is_employee=models.BooleanField('Is employee',default=False)

# class UserManager(BaseManager):
#     def create_user(self, username, p)

class Category(models.Model):
    category = models.CharField( max_length=255)
    categor_id = models.IntegerField()
    slug = models.SlugField(max_length=200 , blank=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category,self).save(*args, **kwargs)
    
    def __str__(self):
        return self.category_name


class QuantityVariant(models.Model):
    variant_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.variant_name

#for image upload
def upload_to(instance,filename):
    return 'posts/{filename}'.format(filename=filename)


class products(models.Model):
    id = models.AutoField(primary_key=True)
    products = models.CharField( max_length=255)
    product_Code=models.IntegerField(unique=True)
    category = models.CharField(max_length=255)
    #quantity_variant = models.ForeignKey(QuantityVariant, on_delete=models.CASCADE)
    #cat1 = models.ForeignKey('groceryapp.Category', on_delete=models.PROTECT)
    #category_id = models.ForeignKey('Category', on_delete=models.CASCADE)
    price=models.IntegerField()
    weight = models.CharField(max_length=255)
    image=models.ImageField(_("IMAGE"),upload_to=upload_to)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quantity_type = models.ForeignKey(QuantityVariant , blank=True, null=True , on_delete=models.PROTECT)

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    products = models.CharField( max_length=2555)
    product_Code=models.IntegerField(unique=True)
    price=models.IntegerField()
    qty=models.IntegerField()
    customer_id=models.ForeignKey('User', on_delete=models.CASCADE,related_name='cart1')

class orders(models.Model):
    id = models.AutoField(primary_key=True)
    username=models.CharField(max_length=255)
    products = models.CharField( max_length=255)
    product_Code=models.IntegerField(unique=True)
    address1 = models.CharField( max_length=255) 
    address2 = models.CharField( max_length=255) 
    address3 = models.CharField( max_length=255)
    state=models.CharField(max_length=30)
    place = models.CharField(max_length=25)
    pincode=models.IntegerField()
    pmmode = models.CharField(max_length=255)
    price=models.IntegerField()
    order_status = models.CharField(max_length=255)
    email = models.EmailField(verbose_name='email address', max_length=255,unique=True)
    phno=models.IntegerField()
    qty=models.IntegerField()
    customer_id=models.ForeignKey('User', on_delete=models.CASCADE,related_name='orders1')
    is_cancel=models.IntegerField(default=0)
    #order_id = models.Random()
    #delivery_status=models.BooleanField(default=False)


class deliverAddresstable(models.Model):
    id = models.AutoField(primary_key=True)
    username=models.CharField(max_length=255)
    # products = models.CharField( max_length=255)
    # product_Code=models.IntegerField(unique=True)
    address1 = models.CharField( max_length=255) 
    address2 = models.CharField( max_length=255) 
    address3 = models.CharField( max_length=255)
    state=models.CharField(max_length=30)
    place = models.CharField(max_length=25)
    pincode=models.IntegerField()
    pmmode = models.CharField(max_length=255)
    price=models.IntegerField()
    order_status = models.CharField(max_length=255)
    email = models.EmailField(verbose_name='email address', max_length=255,unique=True)
    phno=models.IntegerField()
    qty=models.IntegerField()
    #customer_id=models.ForeignKey('User', on_delete=models.CASCADE)
    # is_cancel=models.IntegerField(default=0)   
    
class delivery_assigned(models.Model):
    id = models.AutoField(primary_key=True)
    username=models.CharField(max_length=255)
    products = models.CharField( max_length=2555)                            
    product_order_id=models.IntegerField(unique=True)
    assigned = models.CharField( max_length=255) 
    place_to_deliver = models.CharField( max_length=255) 
    delivery_time_planned = models.DateField( ) 
    amount_recived=models.IntegerField()    
    customer_id=models.ForeignKey('User', on_delete=models.CASCADE)
    
    
class delivery(models.Model):
    id = models.AutoField(primary_key=True)
    delivery_boy_name=models.CharField(max_length=255)
    email = models.EmailField(verbose_name='email address', max_length=255,unique=True)
    phno=models.IntegerField()
    place = models.CharField( max_length=255) 
    address = models.CharField( max_length=255) 
    detail=models.CharField(max_length=255)
    #customer_id=models.ForeignKey('User', on_delete=models.CASCADE)
    






# class Category(models.Model):
#     category = models.CharField( max_length=255)
#     categor_id = models.IntegerField()
    # slug = models.SlugField(max_length=200 , blank=True)
    
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.category_name)
    #     super(Category,self).save(*args, **kwargs)
    
    # def __str__(self):
    #     return self.category_name



# class UserManager(BaseUserManager):
#     """Class to manage the creation of user objects"""

#     def create_user(self, username, email,phno, password=None):
#         """Creates and returns a user object
#         Arguments:
#         username: the string to use as username
#         email: the string to use as email
#         password: the string to use as password

#         Optionals:
#         is_staff: Boolean to indicate a user is staff or not
#         is_admin: Boolean to indicate a user is an admin or not
#         is_active: Boolean to indicate a user can login or not

#         Return:
#             A user object
#         """
#         if not username:
#             raise ValueError('Users must have a username')

#         if not email:
#             raise ValueError('Users must have an email address')

#         if not password:
#             raise ValueError('Users must have a password')

        
#         user = self.model(username=username,email = self.normalize_email(email),)
#         user.set_password(password)
#         user.set_phno(phno)
#         user.is_active=True
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, email,phno, password):
#         """Creates an admin user object
#         Arguments:
#         username: the string to use as username
#         email: the string to use as email
#         password: the string to use as password

#         Return:
#             A user object
#         """
#         user = self.create_user(username, email,phno, password=password)
#         user.is_admin=True
#         user.save(using=self._db)
#         return user


# class User(AbstractBaseUser, PermissionsMixin):
#     """
#     Class for creating user implementing the abstract
#     base user and the permission class
#     """
#     username = models.CharField(max_length=255, unique=True)
#     email = models.EmailField(verbose_name='email address', max_length=255,unique=True)
#     phno=models.IntegerField(max_length=10)
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']

#     objects = UserManager()

#     def __str__(self):
#         """Returns a string representation of this `User`."""
#         return self.username

#     def delete(self, using=None, keep_parents=False):
#         self.is_active ^= True
#         self.save()

#     def get_full_name(self):
#         # The user is identified by their email address
#         return self.username

#     def get_short_name(self):
#         # The user is identified by their email address
#         return self.username

#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         return True

#     def has_module_perms(self, app_label):
#         "Does the user have permissions to view the app `app_label`?"
#         return True

#     @property
#     def is_staff(self):
#         "Is the user a member of staff?"
#         return self.is_admin

# class Role(Group):
#     description = models.TextField(max_length=100, unique=True)

#     def __str__(self):
#         """Returns a string representation of this `Role`."""
#         return self.name



    