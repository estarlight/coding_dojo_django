from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^wall$', views.wall, name='wall'),
    url(r'^register$', views.register, name='register'),
    url(r'login$', views.login, name='login'),
    url(r'^post/message', views.post_message),
    url(r'post/(?P<id>\d+)$', views.post_comment),
    url(r'^logoff', views.logoff),
    url(r'^delete/(?P<id>\d+)$', views.delete)
]