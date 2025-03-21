from django.contrib.auth.models import AbstractUser

from byuhbll_django_dry.models import UserMixin


class User(AbstractUser, UserMixin):
    pass
