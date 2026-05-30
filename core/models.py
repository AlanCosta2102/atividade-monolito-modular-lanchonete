from django.db import models


from django.db import models

# Create your models here.

import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from .manager import SoftDeleteManager,UserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core import validators,mail
from django.utils.translation import gettext_lazy as _


# Create your models here.

from django.utils import timezone
import re

class User(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(_('username'), max_length=15, unique=True, help_text=_('Required. 15 characters or fewer. Letters, numbers and @/./+/-/_ characters'), validators=[ validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), _('invalid'))])    
    first_name = models.CharField(_('first name'), max_length=30)    
    last_name = models.CharField(_('last name'), max_length=30)    
    email = models.EmailField(_('email address'), max_length=255, unique=True)    
    is_staff = models.BooleanField(_('staff status'), default=False, help_text=_('Designates whether the user can log into this admin site.'))    
    is_active = models.BooleanField(_('active'), default=True, help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    is_superuser = models.BooleanField(default=False)
    
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_trusty = models.BooleanField(_('trusty'), default=False, help_text=_('Designates whether this user has confirmed his account.'))

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        
    def get_full_name(self):
            full_name = '%s %s' % (self.first_name, self.last_name)
            return full_name.strip()
    def get_short_name(self) -> str:
        return self.first_name
    def email_user(self, subject, message, from_email=None) -> str:
        mail.send_mail(subject, message, from_email, [self.email])


def get_sentinel_user():
    return User.objects.get_or_create(email="deleted")[0]


class UUIDModel(models.Model):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)

    class Meta:
        abstract = True

class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    objects = SoftDeleteManager()
    all_objects = (
        models.Manager()
    )  

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    class Meta:
        abstract = True


class CreationTimestampedModel(models.Model):
    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
        editable=False,
    )
    created_by = models.ForeignKey(
        User,
        verbose_name=_("Created by"),
        on_delete=models.SET(get_sentinel_user),
        null=True,
        editable=False, # Resolvido na raiz!
        related_name="created_%(app_label)s_%(class)s_set",
    )

    class Meta:
        abstract = True


class UpdateTimestampedModel(models.Model):
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True, editable=False)
    updated_by = models.ForeignKey(
        User,
        verbose_name=_("Updated by"),
        on_delete=models.SET(get_sentinel_user),
        null=True,
        related_name="updated_%(app_label)s_%(class)s_set",
    )

    class Meta:
        abstract = True


class TimestampedModel(CreationTimestampedModel, UpdateTimestampedModel):
    class Meta:
        abstract = True


class BaseModel(UUIDModel, TimestampedModel):
    class Meta:
        abstract = True


class BaseModelWithSoftDelete(BaseModel, SoftDeleteModel):
    class Meta:      
        abstract = True



class Item(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=3)
    descricao = models.TextField()

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    data_pedido = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.nome}"