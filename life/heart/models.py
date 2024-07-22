from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Permission
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from .choices import *
from django.conf import settings
User = settings.AUTH_USER_MODEL


def validate_file_size(value):
	from django.core.exceptions import ValidationError
	filesize = value.size
	if filesize > 5242880:
		raise ValidationError("The Maximum filesize that can be uploaded is 5MB.")
	else:
		return value

class Base(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	class Meta:
		abstract = True

class MyAccountManager(BaseUserManager):
	def create_user(self, username, email, password, phone, pin=None, **extra_fields):
		if not username:
			raise ValueError("User must have username!")
		if not email:
			raise ValueError("User must have email!")

		user = self.model(email=self.normalize_email(email),username=username,phone=phone,
							pin=pin,password=password, **extra_fields)
						
		user.set_password(password)
		user.save(using=self._db)
		return user


	def create_superuser(self, email, username, password, phone, **extra_fields):

		user = self.create_user(email=self.normalize_email(email), username=username, password=password,phone=phone, 
							**extra_fields)
		user.is_admin = True				
		user.is_staff = True				
		user.is_superuser = True				
		user.save(using=self._db)
		return user		


class UserProfile(AbstractBaseUser):
	email 		= models.EmailField(verbose_name="email", max_length=60, unique=True, null=True, blank=True)
	username 	= models.CharField(max_length=30, unique=True)
	password 	= models.CharField(max_length=100, null=True, blank=True)
	phone 		= models.CharField(max_length=20, null=True, unique=True)
	date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login 	= models.DateTimeField(verbose_name='last login', auto_now=True)

	# All these field are required for custom user model
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_verified = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	# other
	first_name = models.CharField(max_length=30, blank=True, null=True)
	last_name = models.CharField(max_length=30, blank=True, null=True)
	dob = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
	gender = models.CharField(max_length=50, blank=True, null=True)
	bio = models.TextField(max_length=500, blank=True, null=True)
	profile_pic = models.ImageField(blank=True, null=True, upload_to='Profile_Pics')
	cover_pic = models.ImageField(blank=True, null=True, upload_to='cover_photo')
	userstatus = models.IntegerField(choices=STATUS_CHOICE, default=1)
	pin = models.CharField(max_length=6, blank=True, null=True)
	otp = models.CharField(max_length=10, blank=True, null=True)
	terms_privacy = models.BooleanField(default=False)

	objects = MyAccountManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email', 'phone']

	def __str__(self):
		try:
			return str(self.id) #+" "+ str(self.email)
		except:
			return "_"

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True
	
	def tokens(self):
		refresh = RefreshToken.for_user(self)
		return{
			'refresh':str(refresh),
            'access':str(refresh.access_token)
        }
