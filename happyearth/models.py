from django.db import models

class Restaurant(models.Model):
    name =  models.CharField(max_length=50)
    address =  models.CharField(max_length=200)
    price_level = models.IntegerField()

class User(models.Model):
    name =  models.CharField(max_length=50)
    phone =  models.CharField(max_length=50)
    religion = models.CharField(max_length=100)
    not_eat = models.CharField(max_length=200)
    liked_style = models.CharField(max_length=100)
    
class Dish(models.Model):
    name =  models.CharField(max_length=50)
    flavor =  models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    
class Favorites(models.Model):
    dish = models.ForeignKey('Dish', on_delete = models.CASCADE)
    user = models.ForeignKey('User', on_delete = models.CASCADE)
    restaurant = models.ForeignKey('Restaurant', on_delete = models.CASCADE)
    tag =  models.CharField(max_length=50)