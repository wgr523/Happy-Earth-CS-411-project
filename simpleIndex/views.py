from django.http import HttpResponse

from .models import test_0
def index(request):
    all_test = test_0.objects.order_by('-a1')
    output = ''
    if len(all_test)>0:
        output = str(all_test[0].a2)
    return HttpResponse('This test shows one entry in database: ' + output)

# Create your views here.
