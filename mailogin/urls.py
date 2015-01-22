from django.conf.urls import patterns, url

from . import views


start = views.EmailLoginStartView.as_view(
    template_name='mailogin/start.html',
)
stop = views.EmailLoginStopView.as_view(
    template_name='mailogin/stop.html',
)

urlpatterns = patterns('',
    url(r'^start/$', start, name='mailogin_start'),
    url(r'^stop/([\w:-]+)/$', stop, name='mailogin_stop'),
)
