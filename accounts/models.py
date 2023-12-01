from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user



class Account(AbstractBaseUser):
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    username        = models.CharField(max_length=50, unique=True)
    email           = models.EmailField(max_length=100, unique=True)
    phone_number    = models.CharField(max_length=50)

    # required
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active        = models.BooleanField(default=False)
    is_superadmin        = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
    
class Profile(models.Model):
    user = models.OneToOneField(Account,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, null= True)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    image = models.ImageField(upload_to='users/')
    about = models.TextField(max_length=4000 , blank=True , null=True)
    country = models.CharField(max_length=50 ,blank=True, null=True)
    company = models.CharField(max_length=100 ,blank=True, null=True)
    address_line_1 = models.CharField( max_length=50 , blank=True)
    address_line_2 = models.CharField( max_length=50 , blank=True)
    fb_link = models.URLField( max_length=200 , blank=True , null=True)
    twitter_link = models.URLField( max_length=200, blank=True , null=True)
    instagram_link = models.URLField( max_length=200, blank=True , null=True)
    linked_in_link = models.URLField( max_length=200, blank=True , null=True)
    headline = models.CharField(max_length=50 , blank=True, null=True)
    city = models.CharField(max_length=50 ,blank=True, null=True)


    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    def full_address(self):
        return f"{self.country} | {self.city} | {self.address_line_1} {self.address_line_2}"



    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=Account)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)