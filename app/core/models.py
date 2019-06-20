from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import CICharField
from django.contrib.postgres.fields import JSONField
from django.core.validators import MinValueValidator
from django.core.serializers.json import DjangoJSONEncoder


def validate_min_length(description):
    if len(description) > 0 and len(description) < 10:
        raise ValidationError(
            _('description is not up to ten characters'),
            params={'value': description},
        )


class AbstractTimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError(_('Email is required'))

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Creates and saves a super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user


class User(AbstractBaseUser, PermissionsMixin, AbstractTimeStampModel):
    """Custom user model with email support"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Favorite(AbstractTimeStampModel):

    title = models.CharField(max_length=50)

    description = models.TextField(
        blank=True,
        validators=[validate_min_length])

    ranking = models.IntegerField(validators=[MinValueValidator(1)])

    metadata = JSONField(default=dict, encoder=DjangoJSONEncoder)

    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='favorites')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'title'],
                name='unique_title'),
        ]

    def __str__(self):
        return self.title


class Category(AbstractTimeStampModel):

    name = CICharField(
        db_index=True,
        max_length=50,
        unique=True,
        error_messages={'unique': u'Category name already exists'})

    def __str__(self):
        return self.name
