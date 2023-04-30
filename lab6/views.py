from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as lg, logout as lout

from .models import *
from .forms import *

def index(request):
    if request.user.is_authenticated:
        login = request.user.name + ' ' + request.user.surname
    else:
        login = ''
    return render(request, "lab6/index.html", {'login': login})

def register(request):

    if request.method == "POST":
        try:
            form = RegisterForm(request.POST)
            if form.is_valid():

                email = form['email'].value()
                name = form['name'].value()
                surname = form['surname'].value()
                password = form['password'].value()

                group = User(email=email, name=name, surname=surname, password=password, username=email)
                group.save()
                return redirect('/lab6/')
        except Exception as e:
            return HttpResponse(f"<h1>{e}</h1>")
    else:
        form = RegisterForm()
        return render(request, "lab6/add.html", {'form': form, 'btn_name': 'Register', 'path': ''})

def login(request):
    if request.method == "POST":
        
        form = LoginForm(request.POST)
        if form.is_valid():

            email = form['email'].value()
            password = form['password'].value()

            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_active:
                    lg(request, user)
                    return redirect('/lab6/')
                else:
                    return HttpResponse('Disabled account')
        return redirect('/lab6/')
        
    else:
        form = LoginForm()
        return render(request, "lab6/add.html", {'form': form, 'btn_name': 'Login', 'path': ''})

def logout(request):
    lout(request)
    return redirect('/lab6/')

def table(request, path):
        products = []

        match path:

            case 'users':
                out = User.objects.all()
                for product in out:
                    products.append((
                        product.id,
                        product.email,
                        product.name,
                        product.surname,
                        product.password,
                        product.group_owner,
                        product.admin
                    ))
                names = ['id', 'email', 'name', 'surname', 'password', 'group_owner', 'admin', '']

            case 'groups':
                out = Group.objects.all()
                for product in out:
                    products.append((
                        product.id,
                        product.author.id,
                        product.name
                    ))
                names = ['id', 'author_id', 'name', '']
            
            case 'posts':
                out = Post.objects.all()
                for product in out:
                    products.append((
                        product.id,
                        product.author.id,
                        product.group.id,
                        product.title,
                        product.text,
                        product.date,
                        product.likes,
                    ))
                names = ['id', 'author_id', 'group_id', 'title', 'text', 'date', 'likes', '']
            
            case 'comms':
                out = Comm.objects.all()
                for product in out:
                    products.append((
                        product.id,
                        product.author.id,
                        product.post.id,
                        product.text,
                        product.date,
                        product.likes,
                    ))
                names = ['id', 'author_id', 'post_id', 'text', 'date', 'likes', '']

            case 'emojis':
                out = Emoji.objects.all()
                for product in out:
                    products.append((
                        product.id,
                        product.code,
                        product.value,
                    ))
                names = ['id', 'code', 'value', '']
            
            case 'post_emojis':
                out = Post_Emoji.objects.all()
                for product in out:
                    products.append((
                        product.id,
                        product.post.id,
                        product.emoji.id,
                        product.user.id
                    ))
                names = ['id', 'post_id', 'emoji_id', 'user_id', '']

        return render(request, "lab6/table.html", {'products': products, 'names': names, 'path': path})

def create(request, path):
    if request.method == "POST":
        try:
            match path:

                case 'users':
                    form = UserForm(request.POST)
                    if form.is_valid():

                        name = form['name'].value()
                        surname = form['surname'].value()
                        group_owner = form['group_owner'].value()
                        email = form['email'].value()
                        password = form['password'].value()
                        admin = form['admin'].value()

                        user = User(name=name, surname=surname, group_owner=group_owner, email=email, password=password, 
                        admin=admin, username=email)
                        user.save()

                case 'groups':
                    form = GroupForm(request.POST)
                    if form.is_valid():

                        name = form['name'].value()
                        id = form['author_id'].value()
                        author = User.objects.get(id=id)

                        group = Group(name=name, author=author)
                        group.save()

                case 'posts':
                    form = PostForm(request.POST)
                    if form.is_valid():

                        group_id = form['group_id'].value()
                        author_id = form['author_id'].value()
                        title = form['title'].value()
                        text = form['text'].value()
                        likes = form['likes'].value()

                        group = Group.objects.get(id=group_id)
                        author = User.objects.get(id=author_id)
                        
                        post = Post(author=author, group=group, title=title, text=text, likes=likes)
                        post.save()

                case 'comms':
                    form = CommForm(request.POST)
                    if form.is_valid():

                        post_id = form['post_id'].value()
                        author_id = form['author_id'].value()
                        text = form['text'].value()
                        likes = form['likes'].value()

                        post = Post.objects.get(id=post_id)
                        author = User.objects.get(id=author_id)
                        
                        comm = Comm(author=author, post=post, text=text, likes=likes)
                        comm.save()

                case 'emojis':
                    form = EmojiForm(request.POST)
                    if form.is_valid():

                        code = form['code'].value()
                        value = form['value'].value()
                        
                        emoji = Emoji(code=code, value=value)
                        emoji.save()

                case 'post_emojis':
                    form = Post_EmojiForm(request.POST)
                    if form.is_valid():

                        post_id = form['post_id'].value()
                        author_id = form['author_id'].value()
                        emoji_id = form['emoji_id'].value()

                        post = Post.objects.get(id=post_id)
                        author = User.objects.get(id=author_id)
                        emoji = Emoji.objects.get(id=emoji_id)
                        
                        post_emoji = Post_Emoji(user=author, post=post, emoji=emoji)
                        post_emoji.save()

            return redirect('/lab6/' + path)
        except Exception as e:
            return HttpResponse(f"<h1>{e}</h1>")
    else:
        match path:
            case 'users':
                form = UserForm()
            case 'groups':
                form = GroupForm()
            case 'posts':
                form = PostForm()
            case 'comms':
                form = CommForm()
            case 'emojis':
                form = EmojiForm()
            case 'post_emojis':
                form = Post_EmojiForm()
        return render(request, "lab6/add.html", {'form': form, 'btn_name': 'Create', 'path': path})

def update(request, path, id):
    if request.method == "POST":
        try:
            match path:
                case 'users':
                    form = UserForm(request.POST)
                    if form.is_valid():

                        name = form['name'].value()
                        surname = form['surname'].value()

                        User.objects.filter(id=id).update(name=name, surname=surname)
                case 'groups':
                    form = GroupForm(request.POST)
                    if form.is_valid():

                        name = form['name'].value()
                        author_id = form['author_id'].value()

                        author = User.objects.get(id=author_id)

                        Group.objects.filter(id=id).update(name=name, author=author)
                case 'posts':
                    form = PostForm(request.POST)
                    if form.is_valid():

                        group_id = form['group_id'].value()
                        author_id = form['author_id'].value()
                        title = form['title'].value()
                        text = form['text'].value()
                        likes = form['likes'].value()

                        group = Group.objects.get(id=group_id)
                        author = User.objects.get(id=author_id)

                        Post.objects.filter(id=id).update(text=text, author=author, title=title, likes=likes)
                case 'comms':
                    form = CommForm(request.POST)
                    if form.is_valid():

                        post_id = form['post_id'].value()
                        author_id = form['author_id'].value()
                        text = form['text'].value()
                        likes = form['likes'].value()

                        post = Post.objects.get(id=post_id)
                        author = User.objects.get(id=author_id)

                        Comm.objects.filter(id=id).update(author=author, post=post, text=text, likes=likes)
                case 'emojis':
                    form = EmojiForm(request.POST)
                    if form.is_valid():

                        code = form['code'].value()
                        value = form['value'].value()

                        Emoji.objects.filter(id=id).update(code=code, value=value)
                case 'post_emojis':
                    form = Post_EmojiForm(request.POST)
                    if form.is_valid():

                        post_id = form['post_id'].value()
                        author_id = form['author_id'].value()
                        emoji_id = form['emoji_id'].value()

                        post = Post.objects.get(id=post_id)
                        author = User.objects.get(id=author_id)
                        emoji = Emoji.objects.get(id=emoji_id)

                        Post_Emoji.objects.filter(id=id).update(user=author, post=post, emoji=emoji)
            return redirect('/lab6/' + path)
        except Exception as e:
            return HttpResponse(f"<h1>{e}</h1>")
    else:
        match path:
            case 'users':
                form = UserForm()
            case 'groups':
                form = GroupForm()
            case 'posts':
                form = PostForm()
            case 'comms':
                form = CommForm()
            case 'emojis':
                form = EmojiForm()
            case 'post_emojis':
                form = Post_EmojiForm()
        return render(request, "lab6/add.html", {'form': form, 'btn_name': 'Edit', 'path': path})

def delete(request, path, id):
    try:
        match path:
            case 'users':
                user = User.objects.get(id=id)
                user.delete()
            case 'groups':
                group = Group.objects.get(id=id)
                group.delete()
            case 'posts':
                post = Post.objects.get(id=id)
                post.delete()
            case 'comms':
                comms = Comm.objects.get(id=id)
                comms.delete()
            case 'emojis':
                emojis = Emoji.objects.get(id=id)
                emojis.delete()
            case 'post_emojis':
                post_emojis = Post_Emoji.objects.get(id=id)
                post_emojis.delete()
        return redirect('/lab6/' + path)
    except Exception as e:
        return HttpResponse(f"<h1>{e}</h1>")
