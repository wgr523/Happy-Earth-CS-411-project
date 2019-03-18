from django.urls import path
from django.urls import path, include # new
from django.views.generic.base import TemplateView


from . import views

urlpatterns = [
        path('', views.fake_index, name='index'),
        #path('home', TemplateView.as_view(template_name='registration/home.html'), name='homepage'),
        path('home', views.fake_user, name='homepage'),
        path('r', views.RestaurantIndex.as_view(), name='restaurant index'),
        path('u', views.UserIndex.as_view(), name='user index'),
        path('d', views.DishIndex.as_view(), name='dish index'),
        path('f', views.FavoritesIndex.as_view(), name='favorites index'),
        path('accounts/', include('django.contrib.auth.urls')),
        ]
