from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/v1.0/orders/$', views.OrderView.as_view(), name='add'),

]
