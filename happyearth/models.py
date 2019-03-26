from django.db import models

class Restaurant(models.Model):
    name =  models.CharField(max_length=50)
    address =  models.CharField(max_length=200)
    price_level = models.IntegerField()
    class Meta:
        unique_together = ('name', 'address')

class User(models.Model):
    name =  models.CharField(max_length=50, primary_key=True)
    phone =  models.CharField(max_length=50, blank=True)
    not_eat = models.CharField(max_length=500, blank=True)
    liked_style = models.CharField(max_length=500, blank=True)
    
class Dish(models.Model):
    name =  models.CharField(max_length=50)
    flavor =  models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=500, blank=True)
    
class Favorites(models.Model):
    user = models.ForeignKey('User', on_delete = models.CASCADE)
    restaurant = models.ForeignKey('Restaurant', on_delete = models.CASCADE)
    tag =  models.CharField(max_length=50)
    class Meta:
        unique_together = ('user', 'restaurant', 'tag')

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
    size = models.IntegerField(blank=True, default=1)
    price = models.CharField(max_length=50)
    available = models.BooleanField(default=True)
    ingredient = models.CharField(max_length=500, blank=True)
    class Meta:
        unique_together = ('dish', 'restaurant')
