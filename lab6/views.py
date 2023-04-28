from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import *
from .forms import *

def main(request):
    return render(request, "lab6/main.html")

def user_new(request):
    if request.method == "POST":
        try:
            if request.method == "POST":
                form = UserForm(request.POST)
                if form.is_valid():
                    name = form['name'].value()
                    surname = form['surname'].value()
                    group = User(name=name, surname=surname)
                    group.save()
                    return HttpResponse(f"<h3>id: {group.id} name: {group.name} surname: {group.surname}</h3>")
        except Exception as e:
            return HttpResponse(f"<h1>{e}</h1>")
    else:
        form = UserForm()
        return render(request, "lab6/new.html", {'form': form})

def users(request):

    if request.method == "POST":
        try:
            if request.method == "POST":
                form = UserForm(request.POST)
                if form.is_valid():
                    name = form['name'].value()
                    surname = form['surname'].value()
                    group = User(name=name, surname=surname)
                    group.save()
                    return redirect('/lab6/users')
        except Exception as e:
            return HttpResponse(f"<h1>{e}</h1>")
    else:
        form = UserForm()
    
        out = User.objects.all()
        products = []

        for product in out:
            products.append((
                product.id,
                product.name,
                product.surname
            ))
        return render(request, "lab6/users.html", {'products': products,'form': form})

def groups(request):

    if request.method == "POST":
        try:
            if request.method == "POST":
                form = GroupForm(request.POST)
                if form.is_valid():
                    name = form['name'].value()
                    id = form['author_id'].value()
                    author = User.objects.get(id=id)
                    group = Group(name=name, author=author)
                    group.save()
                    return redirect('/lab6/groups')
        except Exception as e:
            return HttpResponse(f"<h1>{e}</h1>")
    else:
        form = GroupForm()
    
        out = Group.objects.all()
        products = []

        for product in out:
            products.append((
                product.id,
                product.author.id,
                product.name
            ))
        return render(request, "lab6/groups.html", {'products': products,'form': form})

def delete(request, id):
    try:
        group = Group.objects.get(id=id)
        group.delete()
        return redirect('/lab6/groups')
    except Exception as e:
        return HttpResponse(f"<h1>{e}</h1>")

def update(request, id):
    if request.method == "POST":
        try:
            if request.method == "POST":
                form = GroupForm(request.POST)
                if form.is_valid():
                    name = form['name'].value()
                    author_id = form['author_id'].value()
                    author = User.objects.get(id=author_id)
                    Group.objects.filter(id=id).update(name=name, author=author)
                    return redirect('/lab6/groups')
        except Exception as e:
            return HttpResponse(f"<h1>{e}</h1>")
    else:
        form = GroupForm()
        return render(request, "lab6/new.html", {'form': form})

def posts(request):
    if request.method == "POST":
        try:
            if request.method == "POST":
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
                    return redirect('/lab6/posts')
        except Exception as e:
            return HttpResponse(f"<h1>{e}</h1>")
    else:
        form = PostForm()
    
        out = Post.objects.all()
        products = []

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
        return render(request, "lab6/posts.html", {'products': products,'form': form})

def comms(request):
    if request.method == "POST":
        try:
            if request.method == "POST":
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
                    return redirect('/lab6/comms')
        except Exception as e:
            return HttpResponse(f"<h1>{e}</h1>")
    else:
        form = CommForm()
    
        out = Comm.objects.all()
        products = []

        for product in out:
            products.append((
                product.id,
                product.author.id,
                product.post.id,
                product.text,
                product.date,
                product.likes,
            ))
        return render(request, "lab6/comms.html", {'products': products,'form': form})

def emojis(request):
    if request.method == "POST":
        try:
            if request.method == "POST":
                form = EmojiForm(request.POST)
                if form.is_valid():

                    code = form['code'].value()
                    value = form['value'].value()
                    
                    emoji = Emoji(code=code, value=value)
                    emoji.save()
                    return redirect('/lab6/emojis')
        except Exception as e:
            return HttpResponse(f"<h1>{e}</h1>")
    else:
        form = EmojiForm()
    
        out = Emoji.objects.all()
        products = []

        for product in out:
            products.append((
                product.id,
                product.code,
                product.value,
            ))
        return render(request, "lab6/emojis.html", {'products': products,'form': form})

def post_emojis(request):
    if request.method == "POST":
        try:
            if request.method == "POST":
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
                    return redirect('/lab6/post_emojis')
        except Exception as e:
            return HttpResponse(f"<h1>{e}</h1>")
    else:
        form = Post_EmojiForm()
    
        out = Post_Emoji.objects.all()
        products = []

        for product in out:
            products.append((
                product.id,
                product.post.id,
                product.emoji.id,
                product.user.id
            ))
        return render(request, "lab6/post_emojis.html", {'products': products,'form': form})