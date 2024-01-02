from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify 

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


class Day(models.Model):
    name = models.CharField(max_length=50)
    caption = models.CharField( max_length=5000)
    slug = models.SlugField(null=True,blank=True)

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        super(Day,self).save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse("day_detail", kwargs={"slug": self.slug})
    

    def __str__(self):
        return self.name
    
hours = (
    (2,"2 o'clock"),
    (3,"3 o'clock"),
    (4,"4 o'clock"),
    (5,"5 o'clock"),
    (6,"6 o'clock"),
    (7,"7 o'clock"),
    (8,"8 o'clock"),
    (9,"9 o'clock"),
    (10,"10 o'clock"),
    (11,"11 o'clock"),
    (12,"12 o'clock"),
)

class Book(models.Model):
    user = models.ForeignKey(Account,  on_delete=models.CASCADE)
    day = models.ForeignKey(Day, related_name="book_property",  on_delete=models.CASCADE)
    date = models.IntegerField( choices=hours)


    def __str__(self):
        return str(self.day)

    def save(self, *args, **kwargs):
        # Check if the date has already been booked for the selected day
        existing_book = Book.objects.filter(day=self.day, date=self.date).exists()

        if not existing_book:
            # Date hasn't been booked for the selected day, save the instance
            super().save(*args, **kwargs)
            # Optionally, you can remove the date from choices here as well
        else:
            # Date has already been booked for the selected day, handle this case
            # For simplicity, we'll just print a message here
            print(f"The date {self.date} has already been booked for the day {self.day}.")


    