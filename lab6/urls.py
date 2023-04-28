from django.urls import path
from . import views

app_name = 'lab6'
urlpatterns = [
    path('', views.main, name='index'),
    path('users', views.users, name='users'),
    path('groups', views.groups, name='groups'),
    path('posts', views.posts, name='posts'),
    path('comms', views.comms, name='comms'),
    path('emojis', views.emojis, name='emojis'),
    path('post_emojis', views.post_emojis, name='post_emojis'),
    path('groups/delete/<id>', views.delete, name='delete'),
    path('groups/update/<id>', views.update, name='update'),
]