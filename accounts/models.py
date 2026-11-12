from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    profile_picture=models.ImageField(_('profile picture'), null=True, blank=True, upload_to='img/profile_pic')
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    Messsage_preview = models.JSONField(_('messages preview'),null=True, blank=True)
    username=models.CharField(_('username'), unique=True)
    email_verified=models.BooleanField(default=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
class Profile(models.Model):
    profile=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(unique=True, null=True,blank=True, region='US')
    date_modified= models.DateTimeField(auto_now=True)
    status=models.TextField()
    profile_picture = models.ImageField(null=True, blank=True, upload_to="images/profile_pic")


    def __str__(self) :
        return f"{self.profile.first_name} - {self.phone_number}"
    
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(profile=instance)
post_save.connect(create_profile, sender=CustomUser)

