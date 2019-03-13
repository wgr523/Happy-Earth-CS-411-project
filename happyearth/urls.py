from django.urls import path

from . import views

urlpatterns = [
        path('', views.fake_index, name='index'),
        path('r', views.RestaurantIndex.as_view(), name='restaurant index'),
        ]
