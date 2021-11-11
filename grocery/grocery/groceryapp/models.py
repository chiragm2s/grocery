from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractUser,
    PermissionsMixin,
    Group,
)
from django.db.models.fields import AutoField
from django.db.models.manager import BaseManager
class User(AbstractUser):
    is_admin=models.BooleanField('Is admin',default=False)
    is_customer=models.BooleanField('Is customer',default=False)
    phno=models.IntegerField()
    #is_employee=models.BooleanField('Is employee',default=False)

# class UserManager(BaseManager):
#     def create_user(self, username, p)


class products(models.Model):
    id = models.AutoField(primary_key=True)
    products = models.CharField( max_length=2555)
    product_Code=models.IntegerField(unique=True)
    price=models.IntegerField()
    weight = models.CharField(max_length=255)
    image=models.ImageField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    products = models.CharField( max_length=2555)
    product_Code=models.IntegerField(unique=True)
    price=models.IntegerField()
    qty=models.IntegerField()

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
    order_status = models.CharField(max_length=255)
    email = models.EmailField(verbose_name='email address', max_length=255,unique=True)
    phno=models.IntegerField()
    qty=models.IntegerField()
    
class delivery_assigned(models.Model):
    id = models.AutoField(primary_key=True)
    username=models.CharField(max_length=255)
    products = models.CharField( max_length=2555)                            
    #id,name,assigned,place_to_delivery_time_planned,delivered_time,amount_recived,placed_order_id.
    product_order_id=models.IntegerField(unique=True)
    assigned = models.CharField( max_length=255) 
    place_to_deliver = models.CharField( max_length=255) 
    delivery_time_planned = models.DateField( ) 
    amount_recived=models.IntegerField()
    
class delivery(models.Model):
    id = models.AutoField(primary_key=True)
    delivery_boy_name=models.CharField(max_length=255)
    email = models.EmailField(verbose_name='email address', max_length=255,unique=True)
    phno=models.IntegerField()
    place = models.CharField( max_length=255) 
    address = models.CharField( max_length=255) 
    detail=models.CharField(max_length=255)
    
class Category(models.Model):
    categor_id = models.IntegerField()
    category = models.CharField( max_length=2555)
    
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



    