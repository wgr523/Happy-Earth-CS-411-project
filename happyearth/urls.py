from django.urls import path
from django.urls import path, include # new
from django.views.generic.base import TemplateView


from . import views

urlpatterns = [
        path('', views.fake_index, name='index'),
        #path('home', TemplateView.as_view(template_name='registration/home.html'), name='homepage'),
        path('home/', views.user_home, name='homepage'),
        path('home/favorites/', views.user_favorites, name='user favorites'),
        path('home/favorites/<tag>/', views.user_favorites_tag, name='user favorites tag'),
        path('restaurant/<rid>/', views.restaurant_id, name='restaurant'),
        path('restaurant/<rid>/comment/', views.restaurant_id_comment, name='restaurant comment'),
        path('restaurant/<rid>/favorite/', views.restaurant_id_favorite, name='add restaurant to favorite'),
        path('search/', views.search_result, name='search result'),
        #path('account/', include('django.contrib.auth.urls'), name='account'),
        path('r', views.RestaurantIndex.as_view(), name='restaurant index'),
        path('u', views.UserIndex.as_view(), name='user index'),
        path('d', views.DishIndex.as_view(), name='dish index'),
        path('f', views.FavoritesIndex.as_view(), name='favorites index'),
        ]
