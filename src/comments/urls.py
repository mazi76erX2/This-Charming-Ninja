from django.urls import path
from django.contrib import admin

from .views import (
    comment_thread,
    comment_delete
)

app_name = 'comments'

urlpatterns = [
    path('<int:id>/', comment_thread, name='thread'),
    # re_path('^(?P<id>\d+)/$', comment_thread, name='thread'),

    path('<slug:slug>/delete/', comment_delete, name='delete'),
    # re_path(r'^(?P<slug>[\w-]+)/delete/$', comment_delete),
]