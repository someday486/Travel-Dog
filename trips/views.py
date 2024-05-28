from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    alluser = User.objects.all();
    print(alluser)
    content = {
        'alluser':alluser
    }
    return render(request, 'trips/index.html', content);