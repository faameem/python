from django.conf.urls import url
from . import views

app_name='books'
urlpatterns = [
    url(r'search/$', views.search, name='search'),
    url(r'contact/$', views.contact, name='contact')
]
