from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import *

def fake_index(request):
    return HttpResponse("Happy, earth!")

## def restaurants(request):
##     restaurant_list = Restaurant.objects.values()
##     context = {'restaurant_list': restaurant_list}
##     return render(request, 'happyearth/restaurants.html', context)

class RestaurantIndex(generic.ListView):
    context_object_name = 'restaurant_list'
    def get_queryset(self):
        """Return the last five published questions."""
        return Restaurant.objects.values()
