from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/v1.0/imagecode/$', views.ImageCodeView.as_view()),
    url(r'^api/v1.0/smscode/$', views.SMSCodeView.as_view()),
    url(r'^api/v1.0/register/$', views.RegisterView.as_view()),
]
