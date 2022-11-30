from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Customer, Package, Roomtype, Receipt

# Create your views here.
# @login_required(login_url='/login')
def dashboard(request):

    total_customer = Customer.objects.count()
    total_package = Package.objects.count()
    print(Customer.objects.all().count(), Receipt.objects.all().count())
    if request.method == 'GET':

        receipts = Receipt.objects.all()
        search_key = request.GET.get("search_key")
        
        if search_key:
            customers = Customer.objects.all().filter(fullname__icontains=search_key)
        else:
            customers = Customer.objects.all()

    return render(request, 'dashboard.html', context={
        'customers': customers,
        'receipts': receipts,
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