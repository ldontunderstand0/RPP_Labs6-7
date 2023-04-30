from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff being True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser being True")

        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractUser):
    email = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    group_owner = models.BooleanField()
    admin = models.BooleanField()

    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username


# class User(models.Model):
#     id = models.AutoField(primary_key=True)
#     email = models.CharField(max_length=31, null=False, unique=True) 
#     name = models.CharField(max_length=20, null=False)
#     surname = models.CharField(max_length=20, null=False)
#     password = models.CharField(max_length=20, null=False)


class Group(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=20, null=False, unique=True)


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=20, null=False)
    text = models.CharField(max_length=20, null=False)
    date = models.DateField(auto_now=True)
    likes = models.IntegerField(null=0)


class Comm(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=20, null=False)
    date = models.DateField(auto_now=True)
    likes = models.IntegerField(null=0)


class Emoji(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.IntegerField(null=0)
    value = models.IntegerField(null=0)


class Post_Emoji(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    emoji = models.ForeignKey(Emoji, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
