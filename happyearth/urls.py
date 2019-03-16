from django.urls import path

from . import views

urlpatterns = [
        path('', views.fake_index, name='index'),
        path('r', views.RestaurantIndex.as_view(), name='restaurant index'),
        path('u', views.UserIndex.as_view(), name='user index'),
        path('d', views.DishIndex.as_view(), name='dish index'),
        path('f', views.FavoritesIndex.as_view(), name='favorites index')
        ]
