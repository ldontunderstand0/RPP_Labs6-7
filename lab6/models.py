from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, null=False, unique=True) 
    surname = models.CharField(max_length=20, null=False, unique=True)       


class Group(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=20, null=False, unique=True)


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=20, null=False, unique=True)
    text = models.CharField(max_length=20, null=False, unique=True)
    date = models.DateField(auto_now=True)
    likes = models.IntegerField(null=0)


class Comm(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=20, null=False, unique=True)
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
