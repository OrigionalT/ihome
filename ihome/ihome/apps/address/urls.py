from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/v1.0/areas/$', views.AreaView.as_view(), name='areas'),
]
