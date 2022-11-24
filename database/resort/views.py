from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
# @login_required(login_url='/login')
def dashboard(request):
    
    return render(request, 'dashboard.html')

def room(request):

    return render(request, 'room.html')

def roomtype(request):

    return render(request, 'roomtype.html')

def addroom(request):

    return render(request, 'addroom.html')