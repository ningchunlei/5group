from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    return render(request, 'index.html', {'request':request})

@login_required
def manage(request):
    return render(request, 'manage.html', {'request':request})

