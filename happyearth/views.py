from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.db import connection
from .models import *
import datetime

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [ dict(zip(columns, row)) for row in cursor.fetchall() ]

def fake_index(request):
    return HttpResponse("Happy, earth!")

def user_home(request):
    if request.user.is_authenticated:
        username = request.user.get_username()
        user = User.objects.raw('SELECT name, phone FROM happyearth_user WHERE name=%s LIMIT 1;', [username])
        if len(user)!=1:
#user must fill in the phone, we must update database
            #user = User.objects.raw('SELECT name, phone FROM happyearth_user WHERE name=%s LIMIT 1;', [username])
            #return HttpResponseRedirect('.')
            return HttpResponse('No user data!')
        user_info = {"name":user[0].name, "phone":user[0].phone}
        context = {'user_info': user_info}
        return render(request, 'happyearth/user_home.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))

def user_favorites(request):
    if request.user.is_authenticated:
        username = request.user.get_username()
        user = User.objects.raw('SELECT name, phone FROM happyearth_user WHERE name=%s LIMIT 1;', [username])
        if len(user)!=1:
            return HttpResponse("No this user data.")
        user_info = {"name":user[0].name, "phone":user[0].phone}
        with connection.cursor() as c:
            c.execute('SELECT DISTINCT tag FROM happyearth_favorites WHERE user_id=%s;', [username])
            tags = dictfetchall(c)
        #favorites  = Favorites.objects.raw('SELECT DISTINCT restaurant_id, tag FROM happyearth_favorites, happyearth_restaurant WHERE user_id=%s AND restaurant_id = name;', [username])
        context = {'user_info': user_info, 'tags': tags}
        return render(request, 'happyearth/user_favorites.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))

def user_favorites_tag(request, tag):
    if request.user.is_authenticated:
        username = request.user.get_username()
        user = User.objects.raw('SELECT name, phone FROM happyearth_user WHERE name=%s LIMIT 1;', [username])
        if len(user)!=1:
            return HttpResponse("No this user data.")
        user_info = {"name":user[0].name, "phone":user[0].phone}
        with connection.cursor() as c:
            c.execute('SELECT r.id, r.name, r.address FROM happyearth_favorites f, happyearth_restaurant r WHERE f.user_id=%s AND f.tag=%s AND r.id=f.restaurant_id;', [username, tag])
            restaurants = dictfetchall(c)
        context = {'user_info': user_info, 'restaurants': restaurants}
        return render(request, 'happyearth/restaurant_list.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))

def restaurant_id(request, rid):
    with connection.cursor() as c:
        c.execute('SELECT name, address, price_level FROM happyearth_restaurant WHERE id=%s;', [rid])
        r = dictfetchall(c)[0]
        r['price_level'] = '$'*r['price_level']
        c.execute('SELECT d.name, s.price FROM happyearth_restaurant r, happyearth_dish d, happyearth_serve s WHERE r.id=%s AND s.restaurant_id=r.id AND s.dish_id=d.id AND s.available=True;', [rid])
        d = dictfetchall(c)
        context = {'dishes': d, 'restaurant': r}
    if request.user.is_authenticated:
        username = request.user.get_username()
        user = User.objects.raw('SELECT name, phone FROM happyearth_user WHERE name=%s LIMIT 1;', [username])
        if len(user)!=1:
            return HttpResponse("No this user data.")
        user_info = {"name":user[0].name, "phone":user[0].phone}
        with connection.cursor() as c:
            c.execute('SELECT c.date, c.rating, c.review FROM happyearth_comment c, happyearth_restaurant r WHERE c.user_id=%s AND c.restaurant_id=r.id AND r.id=%s AND c.dish_id IS NULL;', [username, rid])
            comments = dictfetchall(c)
            c.execute('SELECT d.name, c.date, c.rating, c.review FROM happyearth_comment c, happyearth_restaurant r, happyearth_dish d WHERE c.user_id=%s AND c.restaurant_id=r.id AND r.id=%s AND c.dish_id IS NOT NULL AND c.dish_id=d.id;', [username, rid])
            dishes = dictfetchall(c)
            c.execute('SELECT * FROM happyearth_favorites WHERE user_id=%s AND restaurant_id=%s LIMIT 1;', [username, rid])
            if len(c.fetchall())>0:
                is_fav = True
            else:
                is_fav = False
            context.update({'user_info': user_info, 'comments': comments, 'comments_dishes': dishes, 'is_favorite': is_fav })
    return render(request, 'happyearth/restaurant.html', context)

def restaurant_id_comment(request, rid):
    if request.user.is_authenticated:
        username = request.user.get_username()
        user = User.objects.raw('SELECT name, phone FROM happyearth_user WHERE name=%s LIMIT 1;', [username])
        if len(user)!=1:
            return HttpResponse("No this user data.")
        user_info = {"name":user[0].name, "phone":user[0].phone}
        ## Below process comment
        if request.method.upper() == "POST":
            try:
                rating = request.POST['rating']
                dish = request.POST['dish']
                review = request.POST['review']
                date = datetime.datetime.now().strftime("%Y-%m-%d")
                with connection.cursor() as c:
                    if dish == "":
                        c.execute('INSERT INTO happyearth_comment (user_id, restaurant_id, rating, review, date) VALUES (%s, %s, %s, %s, %s);', [user_info['name'], rid, rating, review, date])
                    else:
                        c.execute('INSERT INTO happyearth_comment (dish_id, user_id, restaurant_id, rating, review, date) VALUES (%s, %s, %s, %s, %s, %s);', [dish, user_info['name'], rid, rating, review, date])
                return HttpResponseRedirect('..')
            except:
                return HttpResponse("err")
        ## Process comment ends
        with connection.cursor() as c:
            c.execute('SELECT name, address, price_level FROM happyearth_restaurant WHERE id=%s;', [rid])
            r = dictfetchall(c)[0]
            r['price_level'] = '$'*r['price_level']
            c.execute('SELECT d.id, d.name, s.price FROM happyearth_restaurant r, happyearth_dish d, happyearth_serve s WHERE r.id=%s AND s.restaurant_id=r.id AND s.dish_id=d.id AND s.available=True;', [rid])
            d = dictfetchall(c)
            context = {'user_info': user_info, 'dishes': d, 'restaurant': r}
        return render(request, 'happyearth/restaurant_comment.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))

def restaurant_id_favorite(request, rid):
    if request.user.is_authenticated:
        username = request.user.get_username()
        user = User.objects.raw('SELECT name, phone FROM happyearth_user WHERE name=%s LIMIT 1;', [username])
        if len(user)!=1:
            return HttpResponse("No this user data.")
        user_info = {"name":user[0].name, "phone":user[0].phone}
        ## Below process favorite
        if True:
            with connection.cursor() as c:
                c.execute('INSERT IGNORE INTO happyearth_favorites (user_id, restaurant_id, tag) VALUES (%s, %s, %s);', [user_info['name'], rid, 'default'])
        return HttpResponseRedirect(reverse('user favorites'))
        ## Process ends
    else:
        return HttpResponseRedirect(reverse('login'))

def search_result(request):
    if request.method.upper() == "GET":
        try:
            if 'restaurant' in request.GET:
                r = request.GET['restaurant']
            else:
                r = ''
            if 'address' in request.GET:
                a = request.GET['address']
            else:
                a = None
        except:
            return HttpResponse("err")
        with connection.cursor() as c:
            c.execute('SELECT id, name, address FROM happyearth_restaurant WHERE name LIKE %s;', [r'%'+r+r'%'])
            restaurants = dictfetchall(c)
        context = {'restaurants': restaurants}
    if request.user.is_authenticated:
        username = request.user.get_username()
        user = User.objects.raw('SELECT name, phone FROM happyearth_user WHERE name=%s LIMIT 1;', [username])
        if len(user)!=1:
            return HttpResponse("No this user data.")
        user_info = {"name":user[0].name, "phone":user[0].phone}
        context.update({'user_info': user_info})
    return render(request, 'happyearth/restaurant_list.html', context)

class RestaurantIndex(generic.ListView):
    context_object_name = 'r'
    def get_queryset(self):
        return Restaurant.objects.values()

class UserIndex(generic.ListView):
    context_object_name = 'u'
    def get_queryset(self):
        return User.objects.values()
    
class DishIndex(generic.ListView):
    context_object_name = 'd'
    def get_queryset(self):
        return Dish.objects.values()
    
class FavoritesIndex(generic.ListView):
    context_object_name = 'f'
    def get_queryset(self):
        return Favorites.objects.values()
