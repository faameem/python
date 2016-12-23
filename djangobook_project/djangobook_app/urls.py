from django.conf.urls import url
from . import views

app_name='djangobook_app'
urlpatterns = [
    #url(r'/$', views.hello, name='root'),
    url(r'hello/$', views.hello, name='hello'),
    url(r'time/$', views.current_datetime, name='time'),
    url(r'time/plus/(\d{1,2})/$', views.hours_ahead, name='hours_ahead'),
    url(r'meta/$', views.display_meta, name='meta'),
]
