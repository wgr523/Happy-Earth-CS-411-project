from django.http import HttpResponse

from .models import test_0
def index(request):
    all_test = test_0.objects.order_by('-a1')
    output = ''
    if len(all_test)>0:
        t = all_test[0].a2
        output = str(t)
        test_0(a1 = t+1, a2 = t+1).save()
    else:
        test_0(a1 = 1, a2 = 1).save()
    return HttpResponse('This test shows the entry in database that shows the visited times: ' + output)

# Create your views here.
