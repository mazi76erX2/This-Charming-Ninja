from django.urls import path
from django.contrib import admin

from .views import (
	post_list,
	post_create,
	post_detail,
	post_update,
	post_delete,
	)

app_name = 'posts'

urlpatterns = [
    # ex: /posts/
    path('', post_list, name='list'),
    # ex: /posts/create/
    path('create/', post_create, name='create'),
    # ex: /posts/detail/
    path('<slug:slug>/', post_detail, name='detail'),
    # ex: /posts/edit/
    path('<slug:slug>/edit/', post_update, name='update'),
    # ex: /posts/delete/
    path('<slug:slug>/delete/', post_delete, name='delete'),
]
