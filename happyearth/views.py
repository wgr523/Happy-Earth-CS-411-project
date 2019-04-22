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
        user = User.objects.raw('SELECT name, city, state FROM happyearth_user WHERE name=%s LIMIT 1;', [username])
        if len(user)!=1:
#user must fill in the city, state, we must update database
            #return HttpResponseRedirect('.')
            return HttpResponse('No user data!')
            return render(request, 'happyearth/user_info.html')
        user_info = {"name":user[0].name, "city":user[0].city, "state":user[0].state}
        context = {'user_info': user_info}
        #with connection.cursor() as c:
        #    c.execute('INSERT INTO happyearth_user (user_id, city, state) VALUES (%s, %s, %s);', [user_info['name'], user_info['city'], user_info['state']])
        return render(request, 'happyearth/user_home.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))

def user_favorites(request):
    if request.user.is_authenticated:
        username = request.user.get_username()
        user = User.objects.raw('SELECT name, city, state FROM happyearth_user WHERE name=%s LIMIT 1;', [username])
        if len(user)!=1:
            return HttpResponse("No this user data.")
        user_info = {"name":user[0].name, "city":user[0].city, "state":user[0].state}
        with connection.cursor() as c:
            c.execute('SELECT DISTINCT tag FROM happyearth_favorites WHERE user_id=%s;', [username])
            tags = dictfetchall(c)
        context = {'user_info': user_info, 'tags': tags}
        return render(request, 'happyearth/user_favorites.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))

def user_favorites_tag(request, tag):
    if request.user.is_authenticated:
        username = request.user.get_username()
        user = User.objects.raw('SELECT name, city, state FROM happyearth_user WHERE name=%s LIMIT 1;', [username])
        if len(user)!=1:
            return HttpResponse("No this user data.")
        user_info = {"name":user[0].name, "city":user[0].city, "state":user[0].state}
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
        c.execute('SELECT c.date, c.rating, c.review FROM happyearth_comment c WHERE c.restaurant_id=%s AND c.dish_id IS NULL;', [rid])
        comments = dictfetchall(c)
        context = {'dishes': d, 'restaurant': r, 'comments': comments}
    if request.user.is_authenticated:
        username = request.user.get_username()
        user = User.objects.raw('SELECT name, city, state FROM happyearth_user WHERE name=%s LIMIT 1;', [username])
        if len(user)!=1:
            return HttpResponse("No this user data.")
        user_info = {"name":user[0].name, "city":user[0].city, "state":user[0].state}
        with connection.cursor() as c:
            #c.execute('SELECT c.date, c.rating, c.review FROM happyearth_comment c WHERE c.user_id=%s AND c.restaurant_id=%s AND c.dish_id IS NULL;', [username, rid])
            #comments = dictfetchall(c)
            #c.execute('SELECT d.name, c.date, c.rating, c.review FROM happyearth_comment c, happyearth_dish d WHERE c.user_id=%s AND c.restaurant_id=%s AND c.dish_id IS NOT NULL AND c.dish_id=d.id;', [username, rid])
            #dishes = dictfetchall(c)
            c.execute('SELECT * FROM happyearth_favorites WHERE user_id=%s AND restaurant_id=%s LIMIT 1;', [username, rid])
            if len(c.fetchall())>0:
                is_fav = True
            else:
                is_fav = False
            context.update({'user_info': user_info, 'is_favorite': is_fav })
    return render(request, 'happyearth/restaurant.html', context)

def restaurant_id_edit(request, rid):
    with connection.cursor() as c:
        c.execute('SELECT name, address, price_level FROM happyearth_restaurant WHERE id=%s;', [rid])
        r = dictfetchall(c)[0]
        r['price_level'] = '$'*r['price_level']
        c.execute('SELECT d.name, s.price FROM happyearth_restaurant r, happyearth_dish d, happyearth_serve s WHERE r.id=%s AND s.restaurant_id=r.id AND s.dish_id=d.id AND s.available=True;', [rid])
        d = dictfetchall(c)
        context = {'dishes': d, 'restaurant': r}
    if request.user.is_authenticated:
        username = request.user.get_username()
        user = User.objects.raw('SELECT name, city, state FROM happyearth_user WHERE name=%s LIMIT 1;', [username])
        if len(user)!=1:
            return HttpResponse("No this user data.")
        user_info = {"name":user[0].name, "city":user[0].city, "state":user[0].state}
        with connection.cursor() as c:
            c.execute('SELECT c.id, c.date, c.rating, c.review FROM happyearth_comment c WHERE c.user_id=%s AND c.restaurant_id=%s AND c.dish_id IS NULL;', [username, rid])
            comments = dictfetchall(c)
            #c.execute('SELECT d.name, c.date, c.rating, c.review FROM happyearth_comment c, happyearth_dish d WHERE c.user_id=%s AND c.restaurant_id=%s AND c.dish_id IS NOT NULL AND c.dish_id=d.id;', [username, rid])
            #dishes = dictfetchall(c)
            c.execute('SELECT * FROM happyearth_favorites WHERE user_id=%s AND restaurant_id=%s LIMIT 1;', [username, rid])
            if len(c.fetchall())>0:
                is_fav = True
            else:
                is_fav = False
            context.update({'user_info': user_info, 'is_favorite': is_fav ,'comments': comments})
    return render(request, 'happyearth/restaurant_edit.html', context)

def restaurant_id_comment(request, rid):
    if request.user.is_authenticated:
        username = request.user.get_username()
        user = User.objects.raw('SELECT name, city, state FROM happyearth_user WHERE name=%s LIMIT 1;', [username])
        if len(user)!=1:
            return HttpResponse("No this user data.")
        user_info = {"name":user[0].name, "city":user[0].city, "state":user[0].state}
        ## Below process comment
        if request.method.upper() == "POST":
            try:
                rating = request.POST['rating']
                dish = ""#request.POST['dish']#TODO
                review = request.POST['review']
                date = datetime.datetime.now().strftime("%Y-%m-%d")
                with connection.cursor() as c:
                    if dish == "":
                        c.execute('INSERT INTO happyearth_comment (user_id, restaurant_id, rating, review, date) VALUES (%s, %s, %s, %s, %s);', [user_info['name'], rid, rating, review, date])
                    else:
                        c.execute('INSERT INTO happyearth_comment (dish_id, user_id, restaurant_id, rating, review, date) VALUES (%s, %s, %s, %s, %s, %s);', [dish, user_info['name'], rid, rating, review, date])
                return HttpResponseRedirect('..')
            except:
                return HttpResponse("Error when creating comment.")
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

def restaurant_id_edit_comment(request, rid, cid):
    if request.user.is_authenticated:
        username = request.user.get_username()
        user = User.objects.raw('SELECT name, city, state FROM happyearth_user WHERE name=%s LIMIT 1;', [username])
        if len(user)!=1:
            return HttpResponse("No this user data.")
        user_info = {"name":user[0].name, "city":user[0].city, "state":user[0].state}
        ## Below process comment
        if request.method.upper() == "POST":
            try:
                rating = request.POST['rating']
                dish = ""#request.POST['dish']#TODO
                review = request.POST['review']
                date = datetime.datetime.now().strftime("%Y-%m-%d")
                with connection.cursor() as c:
                    if dish == "":
                        c.execute('UPDATE happyearth_comment SET rating=%s, review=%s, date=%s WHERE id=%s AND user_id=%s;', [rating, review, date, cid, user_info['name']])
                    else:
                        c.execute('UPDATE happyearth_comment SET dish_id=%s, rating=%s, review=%s, date=%s WHERE id=%s AND user_id=%s;', [dish, rating, review, date, cid, user_info['name']])
                return HttpResponseRedirect('..')
            except:
                return HttpResponse("Error when editing comment.")
        ## Process comment ends
        with connection.cursor() as c:
            c.execute('SELECT name, address, price_level FROM happyearth_restaurant WHERE id=%s;', [rid])
            r = dictfetchall(c)[0]
            r['price_level'] = '$'*r['price_level']
            c.execute('SELECT d.id, d.name, s.price FROM happyearth_restaurant r, happyearth_dish d, happyearth_serve s WHERE r.id=%s AND s.restaurant_id=r.id AND s.dish_id=d.id AND s.available=True;', [rid])
            d = dictfetchall(c)
            c.execute('SELECT rating, review, dish_id FROM happyearth_comment WHERE id=%s;', [cid])
            comment = dictfetchall(c)
            if len(comment)!=1:
                return HttpResponse("No such comment.")
#             return HttpResponse(str(comment))
            context = {'user_info': user_info, 'dishes': d, 'restaurant': r, 'comment': comment[0]}
        return render(request, 'happyearth/restaurant_comment.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))
    
def restaurant_id_delete_comment(request, rid, cid):
    if request.user.is_authenticated:
        username = request.user.get_username()
        user = User.objects.raw('SELECT name, city, state FROM happyearth_user WHERE name=%s LIMIT 1;', [username])
        if len(user)!=1:
            return HttpResponse("No this user data.")
        user_info = {"name":user[0].name, "city":user[0].city, "state":user[0].state}
        try:
            with connection.cursor() as c:
                c.execute('DELETE FROM happyearth_comment WHERE id=%s AND user_id=%s;', [cid, user_info['name']])
        except:
            return HttpResponse("Error when deleting comment.")
        return HttpResponseRedirect('../..')
    else:
        return HttpResponseRedirect(reverse('login'))
    
def restaurant_id_favorite(request, rid):
    if request.user.is_authenticated:
        username = request.user.get_username()
        user = User.objects.raw('SELECT name, city, state FROM happyearth_user WHERE name=%s LIMIT 1;', [username])
        if len(user)!=1:
            return HttpResponse("No this user data.")
        user_info = {"name":user[0].name, "city":user[0].city, "state":user[0].state}
        ## Below process favorite
        if True:
            with connection.cursor() as c:
                c.execute('INSERT IGNORE INTO happyearth_favorites (user_id, restaurant_id, tag) VALUES (%s, %s, %s);', [user_info['name'], rid, 'default'])
                c.execute('CALL InsertRecommendRestaurant(%s, %s);', [user_info['name'], rid])
                c.execute('CALL InsertRecommendRestaurant2(%s, %s);', [user_info['name'], rid])
        return HttpResponseRedirect('..')
        ## Process ends
    else:
        return HttpResponseRedirect(reverse('login'))

def search_result(request):
    if request.method.upper() == "GET":
        try:
            if 'restaurant' in request.GET:
                r = request.GET['restaurant'].lower()
            else:
                r = ''
            if 'address' in request.GET:
                a = request.GET['address'].lower()
            else:
                a = ''
        except:
            return HttpResponse("Error. Invalid GET request.")
    if request.user.is_authenticated:
        username = request.user.get_username()
        user = User.objects.raw('SELECT name, city, state FROM happyearth_user WHERE name=%s LIMIT 1;', [username])
        if len(user)!=1:
            return HttpResponse("No this user data.")
        with connection.cursor() as c:
            c.execute('SELECT id, name, address, city, state FROM happyearth_restaurant WHERE city=%s AND state=%s AND lower(name) LIKE %s;', [user[0].city, user[0].state, r'%'+r+r'%'])# we only search restaurant in same city, state
            restaurants = dictfetchall(c)
        user_info = {"name":user[0].name, "city":user[0].city, "state":user[0].state}
        context= {'restaurants': restaurants, 'user_info': user_info}
    else:
        with connection.cursor() as c:
            c.execute('SELECT id, name, address, city, state FROM happyearth_restaurant name LIKE %s;', [r'%'+r+r'%'])
            restaurants = dictfetchall(c)
        context = {'restaurants': restaurants}
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
