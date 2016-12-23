# Projects vs. apps #
+ What’s the difference between a project and an app? An app is a Web application that does something – e.g., a Weblog system, a database of public records or a simple poll app. A project is a collection of configuration and apps for a particular website. A project can contain multiple apps. An app can be in multiple projects.

# Creating a Project #
+ $ django-admin startproject django_project
+ Use Eclipse to create django_project

# Default migration #
+ $ python manage.py migrate

# Development Server #
+ $ python manage.py runserver faisalm-pc1:6666

# Creating an App #
+ $ python manage.py startapp tutorial

# Validate Models #
+ $ python manage.py check

# Make Migrations #
+ $ python manage.py makemigrations tutorial

# Check Migrate SQL #
+ $ python manage.py sqlmigrate tutorial 0001

# Schema Migration #
+ $ python manage.py migrate

# Playing with API #
+ $ python manage.py shell

# django Admin - create admin user #
+ python manage.py createsuperuser
	- faisalm
	- admin12345
+ python manage.py runserver
+ http://localhost:8000/admin

# running tests #
+ $ python manage.py test tutorial

# django_project/templates/admin #
+ Got base_site.html file from Django installed directory (django/contrib/admin/templates), and changed the site header.
+ To see Django source files: $ python -c "import django; print(django.__path__)"

# Reusable apps using packages #
+ [create app package](https://docs.djangoproject.com/en/1.10/intro/reusable-apps/)

# Python Regex Docs #
+ [regex](https://docs.python.org/3.4/library/re.html)