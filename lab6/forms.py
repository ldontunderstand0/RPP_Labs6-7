from django import forms
from .models import User


class LoginForm(forms.Form):
    email = forms.EmailField(label="email", max_length=20)
    password = forms.CharField(label="password", max_length=20, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    email = forms.EmailField(label="email", max_length=20)
    name = forms.CharField(label="name", max_length=20)
    surname = forms.CharField(label="surname", max_length=20)
    password = forms.CharField(label="password", max_length=20, widget=forms.PasswordInput)


class UserForm(forms.Form):
    email = forms.EmailField(label="email", max_length=20)
    name = forms.CharField(label="name", max_length=20)
    surname = forms.CharField(label="surname", max_length=20)
    password = forms.CharField(label="password", max_length=20, widget=forms.PasswordInput)
    group_owner = forms.IntegerField(label="group_owner")
    admin = forms.IntegerField(label="admin")



class GroupForm(forms.Form):
    name = forms.CharField(label="name", max_length=20)
    author_id = forms.IntegerField(label="author_id")


class PostForm(forms.Form):
    group_id = forms.IntegerField(label="group_id")
    author_id = forms.IntegerField(label="author_id")
    title = forms.CharField(label="title", max_length=20)
    text = forms.CharField(label="text", max_length=100)
    likes = forms.IntegerField(label="likes")


class CommForm(forms.Form):
    post_id = forms.IntegerField(label="post_id")
    author_id = forms.IntegerField(label="author_id")
    text = forms.CharField(label="text", max_length=100)
    likes = forms.IntegerField(label="likes")


class EmojiForm(forms.Form):
    code = forms.IntegerField(label="code")
    value = forms.IntegerField(label="value")


class Post_EmojiForm(forms.Form):
    post_id = forms.IntegerField(label="post_id")
    emoji_id = forms.IntegerField(label="emoji_id")
    author_id = forms.IntegerField(label="author_id")
    