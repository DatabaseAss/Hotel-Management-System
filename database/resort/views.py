from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Customer, Package, Roomtype

# Create your views here.
# @login_required(login_url='/login')
def dashboard(request):

    total_customer = Customer.objects.count()
    total_package = Package.objects.count()

    if request.method == 'GET':
        search_key = request.GET.get("search_key")
        
        if search_key:
            customers = Customer.objects.all().filter(fullname__icontains=search_key)
        else:
            customers = Customer.objects.all()

    return render(request, 'dashboard.html', context={
        'customers': customers,
        'total_customers':  total_customer,
        'total_package': total_package
    })

def room(request):

    return render(request, 'room.html')

def roomtype(request):
    
    roomtypes = Roomtype.objects.all()

    return render(request, 'roomtype.html', context = {
        'room_types': roomtypes
    })

def addroom(request):

    return render(request, 'addroom.html')