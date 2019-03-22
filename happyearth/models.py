from django.db import models

class Restaurant(models.Model):
    name =  models.CharField(max_length=50, unique=True)
    address =  models.CharField(max_length=200)
    price_level = models.IntegerField()

class User(models.Model):
    name =  models.CharField(max_length=50, unique=True)
    phone =  models.CharField(max_length=50, blank=True)
    religion = models.CharField(max_length=100, blank=True)
    not_eat = models.CharField(max_length=200, blank=True)
    liked_style = models.CharField(max_length=100, blank=True)
    
class Dish(models.Model):
    name =  models.CharField(max_length=50, unique=True)
    flavor =  models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=500, blank=True)
    
class Favorites(models.Model):
    dish = models.ForeignKey('Dish', on_delete = models.CASCADE, blank=True, null=True)
    user = models.ForeignKey('User', on_delete = models.CASCADE)
    restaurant = models.ForeignKey('Restaurant', on_delete = models.CASCADE)
    tag =  models.CharField(max_length=50)

class Comment(models.Model):
    dish = models.ForeignKey('Dish', on_delete = models.CASCADE, blank=True, null=True)
    user = models.ForeignKey('User', on_delete = models.CASCADE)
    restaurant = models.ForeignKey('Restaurant', on_delete = models.CASCADE)
    rating = models.IntegerField()
    review = models.CharField(max_length=500, blank=True)
    date = models.DateField()

class Serve(models.Model):
    dish = models.ForeignKey('Dish', on_delete = models.CASCADE)
    restaurant = models.ForeignKey('Restaurant', on_delete = models.CASCADE)
    size = models.IntegerField(blank=True)
    price = models.CharField(max_length=50)
    available = models.BooleanField(default=True)
    ingredient = models.CharField(max_length=500, blank=True)
