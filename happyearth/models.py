from django.db import models

class Restaurant(models.Model):
    name =  models.CharField(max_length=50)
    address =  models.CharField(max_length=200)
    city =  models.CharField(max_length=50)
    state =  models.CharField(max_length=20)
    postal_code =  models.CharField(max_length=20)
    price_level = models.IntegerField()
    class Meta:
        unique_together = ('name', 'address', 'city', 'state', 'postal_code')

class Category(models.Model):
    restaurant = models.ForeignKey('Restaurant', on_delete = models.CASCADE)
    category = models.CharField(max_length=50)
    class Meta:
        unique_together = ('restaurant', 'category')

class Hour(models.Model):
    DAYS = (
            ('MON', 'Monday'),
            ('TUE', 'Tuesday'),
            ('WED', 'Wednesday'),
            ('THU', 'Thursday'),
            ('FRI', 'Friday'),
            ('SAT', 'Saturday'),
            ('SUN', 'Sunday'),
            )
    restaurant = models.ForeignKey('Restaurant', on_delete = models.CASCADE)
    day = models.CharField(max_length=3, choices = DAYS)
    hour = models.CharField(max_length=20)
    class Meta:
        unique_together = ('restaurant', 'day')

class User(models.Model):
    name =  models.CharField(max_length=50, primary_key=True)
    city =  models.CharField(max_length=50)
    state =  models.CharField(max_length=20)
    reg_date = models.DateField()
    
class Dish(models.Model):
    name =  models.CharField(max_length=50, primary_key=True)
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
    #size = models.IntegerField(blank=True, default=1)
    #price = models.CharField(max_length=20)
    #available = models.BooleanField(default=True)
    class Meta:
        unique_together = ('dish', 'restaurant')

class Recommend(models.Model):
    user = models.ForeignKey('User', on_delete = models.CASCADE)
    restaurant = models.ForeignKey('Restaurant', on_delete = models.CASCADE)
    class Meta:
        unique_together = ('user', 'restaurant')

class Together(models.Model):
    user = models.ForeignKey('User', on_delete = models.CASCADE, unique = True)
    code = models.IntegerField()
