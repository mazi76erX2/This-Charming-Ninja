# My Workflow for Django

## In command prompt

1. cd into the folder you want to work in.

2. Make Virtual Environment
```console
pip freeze

pip install virtualenv
virtualenv mysiteENV
```


3. Activate Eneviornment
```console
mysiteENV\scripts\activate.dat
```

4. Install Django
```console
pip install django 
```

then install the databse client for Postgres

```console
pip install psycopg2 or

pip install --only-binary :all: mysqlclient
```

or whatever database package you're using.

5.Make sure Django is installed


```console
python -m django --version
``` 

6. To start the project:
```console
django-admin startproject {mysite}
```
then 
```console
cd {mysite}
```

7.This instruction is to check that the setup is running (using 8080 just incase 8000 is being used):
```console
python manage.py runserver 8080
```

8. Create admin:
```console
python manage.py createsuperuser
```

9. To make an app inside the project
```console
python manage.py startapp {app}
``` 

10. make a python file {app}/urls.py.

Make edits to urls in each {app} and {mysite} and edits in views.

### Add in mysite
```python
from django.urls import include, path

path('^{app}/', include('{app}.urls')),
```

### app
```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

Add view in {app}/views.py (Just to test that everything is working. Need this for migration).
```python
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the {app} index.")
```

11. If you're using sqlite3 leave the settings.py file the way it is. If you're using postgres (for example) create the database in the program itself and use the credentials when you add:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'myproject',
        'USER': 'myprojectuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```

---------mysql-setup---------
```console
mysql> CREATE DATABASE <database name>;
```

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'database-name',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

To setup up the Database:
```console
python manage.py migrate
``` 

into the settings file.

12. make models for {app} using [Models](https://docs.djangoproject.com/en/2.1/ref/models/instances/#django.db.models.Model) in {app}/models.py

```python
for example: 
class <Model>(models.Model):
		title = models.CharField(max_length=120)

		def __str__(self):
			return self.title
```

13. Activate models by adding this into INSTALLED_APPS in the settings file:
```python
{app}.apps.{app}Config
```

14. 
```console
python manage.py makemigrations {app}
``` 
Tells django to adds the changes made in models.py to the database. 

```console
python manage.py sqlmigrate {app} 0001
``` 
Shows you all the changes that will be made to the database.

NOTE: Whenever you make changes to the model you must ```makemigrations``` then ```migrate``` (Because you are changing how the database saves the data).

```python 
manage.py migrate
``` 
Again to actually make the changes.

15. Make the app modifiable in the admin by adding the following in the file {app}/admin.py:

```python
from django.contrib import admin
from .models import <Model 1>, <Model 2>


class <Model 1>Admin(admin.ModelAdmin):
    <filter> = [<"model object 1">, <"model object 2">, ...]

    class Meta:
        model = <Model>

admin.site.register(<model 1>, <model 1>ModelAdmin)
```

Eg.
```python
from models import Post


class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title", "updated", "timestamp"]
    list_display_links = ["updated"]
    list_editable = ["title"]
    list_filter = ["updated", "timestamp"]

    search_fields = ["title", "content"]
    class Meta:
        model = Post

admin.site.register(Post, PostModelAdmin)
```

To see more on this go to:
[Admin](https://docs.djangoproject.com/en/2.1/ref/contrib/admin/)

access it by using ```python manage.py runserver 8080``` and ```http://127.0.0.1:8080/admin/```

16. ```python manage.py shell``` to work with the database of the app using django and python commands.

[Tutorial 2 Databases](https://docs.djangoproject.com/en/2.1/intro/tutorial02/)

In command prompt:

```
from polls.models import Question, Choice

Question.objects.all()
```

---OR---

17. ```http://127.0.0.1:8080/admin/``` in web browser to use this platform After ```python manage.py runserver 8080```. Only need to runserver after you make changes to database.

18. Change views in {app}/views.py

[Views](https://docs.djangoproject.com/en/1.11/intro/tutorial03/)

Using the CRUD model, start with:

```python
from .models import {model1}, {model2}, {model3}

def {app}_create(request):
    return HttpResponse("<h1>Create</h1>")


def {app}_detail(request): #retrieve
    return HttpResponse("<h1>Detail</h1>")


def {app}_list(request): #list items
    return HttpResponse("<h1>List</h1>")


def {app}_update(request):
    return HttpResponse("<h1>Update</h1>")


def {app}_delete(request):
    return HttpResponse("<h1>Delete</h1>")
```

In {app}/urls.py:

```python
from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = 'slideshow'

urlpatterns = [
    path('', views.{app}_list, name='list'),
    path('create/', views.{app}_create, name='create'),
    path('detail/', views.{app}_detail, name='detail'),
    path('update/', views.{app}_update, name='update'),
    path('delete/', views.{app}_delete, name='delete'),
]
```

Eventually change to:

```python
urlpatterns = [
    path('', views.{app}_list, name='list'),
    path('create/', views.{app}_create, name='create'),
    path('<slug:slug>/detail/', views.{app}_detail, name='detail'),
    path('<slug:slug>/update/', views.{app}_update, name='update'),
    path('<slug:slug>/delete/', views.{app}_delete, name='delete'),
]
```

And in {mysite}/urls.py:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('{app}/', include("{app}.urls", namespace='{app}')),
]
```

Then develop these views for example:

```python
def {app}_detail(request, id=None):
    instance = get_object_or_404(<Model>, id=id)
    context = {
        "title": instance.title,
        "instance": instance,
    }
    return render(request, "{app}_detail.html", context)
```

Make templates to relate these changes in new folder 'templates' in the project folder and 'index.html' etc.

example for {app}_detail:
```html
<!DOCTYPE html>
<html>
<body>
{% if messages %}
<ul class="messages">
    {% for message in messages %}
    <li {% if message.tags %} class="{{ message.tags }}"{% endif %}>{% if "html_safe" in message.tags %}{{ message|safe }}{% else %}{{ message }}{% endif %}</li>
    {% endfor %}
</ul>
{% endif %}
<h1>{{ title }}</h1>
{{ instance.title }}<br/>
{{ instance.content }}<br/>
{{ instance.timestamp }}<br/>
{{ instance.updated }}<br/>
{{ instance.id }}<br/>
</body>
</html>
```

in templates/{app}_detail.html
Add in {mysite}/settings.py TEMPLATES -> DIRS:
```python 
os.path.join(BASE_DIR, 'templates')
```

Look at [Generic views](https://docs.djangoproject.com/en/2.1/topics/class-based-views/generic-display/)

If your using forms

19. Make a form in {app}/form.py using:

[Forms](https://docs.djangoproject.com/en/1.11/topics/forms/) and
[Form Model](https://docs.djangoproject.com/en/1.11/topics/forms/modelforms/#modelform)

Make a template in templates/form_{app}.html

```python
from django import forms
from .models import <model 1>, <model 2>.....


class {model}Form(forms.ModelForm):
    publish = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = <model 1>
        fields = [
            "<field 1 in model 1>",
            "<field 2 in model 1>",
            ....
        ]
```
In views.py:

```python
form = <model>Form(request.POST or None)

if form.is_valid():
    <field 1 in model 1> = form.save(commit=False)
    <field 1 in model 1>.save()
    return HttpResponseRedirect(instance.get_absolute_url())

context = {
    "form": form,
    ...
}
return render(request, "<form_name>.html", context)
```
Make a new template in templates/<form_name>.html
```html
...
<form method='POST' action=''>
{% csrf_token %}
{{ form.as_p }}
<input type='submit' value='<Button name' />
</form>
...
```
When creating an update combine this form view with detail view.

20. Create a flash message

in views.py add: 

```python
from django.contrib import messages
...

messages.success(request, "<message>")
messages.error(request, "<message>")
```

and into your templates:

```html
{% if messages %}
<ul class="messages">
    {% for message in messages %}
    <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
    {% endfor %}
</ul>
{% endif %}
```

21. When creating a delete view:

```python
def {app}_delete(request, id=None):
    instance = get_object_or_404(Post, id=id)
    instance.deleted()
    messages.success(request, "<message>")
    return redirect("<other view>")
```

in views.py

And edit the url in urlpatterns app/urls.py. For example:

```python
path('delete/', views.delete, name='delete'),
```

23. Make a 'parent template' for all the templates of the app.

Dont forget to change the render url in views.py

Add:

```html
<head>
	<title>{% block head_title %}Title{% endblock head_title %}</title>
</head>
...

<div class="container">
{% block content %}

<parent html files content>

{% endblock content %}
```

in the parent template 'base.html' then make a new template for index

Then add:

```html
{% block head_title %}{{ instance.title }} | {{ block.super }}{% endblock head_title %}

...

{% extends "base.html" %}

{% block content %}

<contents of other templates>

{% endblock content %}'
```

to all the other templates.

24. Make static files for the project [Static files](https://docs.djangoproject.com/en/1.11/howto/static-files/)

Add in the settings.py file under STATIC_URL: 
```python
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    #'/var/www/static/',
]

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn")
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media_cdn")
```

in {mysite}/urls.py Add:

```python
from django.conf import settings
from django.conf.urls.static import static
...
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```



Create 3 new folders. '{Base directory}/static_cdn', '{Base directory}/media_cdn' and '{app}/static'

Then type ```python manage.py collectstatic``` in cmd. Type yes and all the files should be added to the static_cdn.

Add more static files to the 'src/static' folder. 
add the link in the head of the template. 

```html
{% load staticfiles %}
...
<link rel="stylesheet" type="text/css" href="{% static /css/base.css %}">
...
<img src='{% static "img/somepicture.jpg" %}'>
```

and when you're done collectstatic again. This simulates sending static files to the server.

{{ STATIC_URL }}
25. Add bootstrap/materialize as the css framework for easy front end development into the {app}/static folder.


26. If you're making a webapp with multiple pages use pagination.

Add to views.py: 

```python
paginator = Paginator(<queryset>_list, 10)  # Show 10 posts per page
page_request_var = 'page'
page = request.GET.get(page_request_var)
try:
    <queryset> = paginator.page(page)
except PageNotAnInteger:
    # If page is not an integer, deliver first page.
    <queryset> = paginator.page(1)
except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
    <query_set> = paginator.page(paginator.num_pages)
```
Add to {app}/templates/<queryset>_list.html:

```html
<div class="pagination">
    <span class="step-links">
        {% if post_list.has_previous %}
            <a href="?{{ page_request_var }}={{ posts_list.previous_page_number }}">previous</a>
        {% endif %}

        <span class="current">
            Page {{ <queryset>_list.number }} of {{ <queryset>_list.paginator.num_pages }}.
        </span>

        {% if <queryset>_list.has_next %}
            <a href="?{{ <queryset>_request_var }}={{ <queryset>_list.next_page_number }}">next</a>
        {% endif %}
    </span>
</div>
```
after the for loop of the queryset.

27. When adding images add the field "image = models.ImageField(null=True, blank=True)" in models.py

```console
pip install pillow
```

Add to {app}/urls.py:

```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

Add to settings.py:
```python
MEDIA_URL = "/media/"
...
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media_cdn")
```

Add in forms.py:

'image' to fields list 

And add in {app}_form.html:
```html
<form method='POST' action='' enctype="multipart/form-data">"
```
And finally in {app}_detail.html and {app}_list.html:

```html
{% if instance.image %}
<img src="{{ instance.image.url }}" class='img-responsive'/>
{% endif %}"
```

28. When creating changes to the database you want to make changes to your database then delete database, media_cdn, and migrations in your {app}/migrations/ folder.

    then type: ```python manage.py migrate```, ```python manage.py makemigrations```, ```python manage.py migrate``` and ```python manage.py createsuperuser``` in cmd.

29. Make a slugfield for posts. This changes the link from "{app}/1" to "{app}/first-post"

First add to models.py:

```python
def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    #  If the title is "First Post 1" -> "first-post-1"
    querySet = Post.objects.filter(slug=slug).order_by("-id")
    exists = querySet.exists()
    if exists:
        new_slug = "%s-%s" %(slug, querySet.first().id)
        return create_slug(instance, new_slug=new_slug)
        # "first-post-1-23" if its id is 23
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)
```

Then change get_absolute_url to:

```python
def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug": self.slug})"
```

Changes it from id to slug

Then change the urlpatterns in {app}/urls.py to:
    ```python
    path('<slug:slug>', views.{app}_detail, name='detail')
    ```

Then finally change in views.py:

```python
def {app}_detail(request, slug=None):  # retrieve
    instance = get_object_or_404(Post, slug=slug)
    ...
```
and do the same for any other views that has id instead of slug.

30. 
To Start BrowserSync
1. To Start BrowserSync: ```browser-sync start --server --files "**/*"```
2. To Start BrowserSync for Javascript: ```browser-sync start --server --directory``` --files "**/*"
Type localhost:3000 in browser

31. When making custom template tags create a new folder called templatetages in src and create a __init__.py and urlify.p file inside that folder. 

in urlify.py write:

```python
from urllib.parse import quote
from django import template

register = template.Library()

@register.filter
def urlify(value):
    return quote(value)
```

// TODO: 32. Search

33. To add a markdown editor to your form in stackoverflow style

Add to the base template:

```javascript
<script type="text/javascript">
		$(document).ready(function(){
			$(".content-markdown").each(function(){
					var content = $(this).text()
					console.log(content)
					var markedContent = marked(content)
					console.log(markedContent)
					$(this).html(markedContent)
			})
		})
```
As well as:
```html
<script src="{% static 'js/marked.min.js' %}"></script>
```
OR
```html
<script src='https://cdnjs.cloudflare.com/ajax/libs/marked/0.3.5/marked.min.js'></script>
```

In your detail template add:

```html
<div class='content-markdown'>{{ instance.content }}</div>
```

### A better implementation can be acheived using Django-Markdown
[Django Pagedown](https://github.com/timmyomahony/django-pagedown)

```console
pip install django-pagedown
```

Under INSTALLED_APPS in {blog}/settings.py add:

```python
'pagedown'
```
Then type ```python manage.py collectstatic``` in cmd.

In {app}/admin.py to al markdown capabilities to all textfields add:

```python
from pagedown.widgets import AdminPagedownWidget

class AlbumAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget },
    }
```

in {app}/forms.py

```python
from pagedown.widgets import PagedownWidget

{Textfield} = forms.CharField(widget=PagedownWidget())
```

in the base template between the head tags add:

```python
{% block head_extra %} {% endblock head_extra %}
```

in the form template before the block content tag:

```python
{% block head_extra %}
{{ form.media}}
{% endblock head_extra %}
```
