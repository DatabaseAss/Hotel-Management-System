from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Customer, Package, Roomtype, Receipt, Branch, Bedinfo, SupplyInRoom
from django.contrib import messages
# Create your views here.
def home(request):
    return redirect('/branch/1')

@login_required(login_url='/login')
def dashboard(request, branch):

    total_customer = Customer.objects.count()
    total_package = Package.objects.count()
    print(Customer.objects.all().count(), Receipt.objects.all().count())

    num_branch = 0
    for _, _ in enumerate(Branch.objects.all()):
        num_branch += 1
    branches_link = ["/branch/" + str(x) for x in range(1,num_branch)]

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
        'total_package': total_package,
        'branches': branches_link,
        'branch': branch
    })

def room(request):

    return render(request, 'room.html')

def roomtype(request):
    
    roomtypes = Roomtype.objects.all()

    return render(request, 'roomtype.html', context = {
        'room_types': roomtypes
    })

def addroom(request):
    if request.method == "POST":

        room_type_area = request.POST['area']
        room_type_des = request.POST['description']
        room_type_cap = request.POST['capacity']
        room_type_name = request.POST['roomtypename']
        try:
            new_room_type = Roomtype.objects.create(
                typename = room_type_name,
                area = float(room_type_area),
                capacity = room_type_cap,
                descriptions = room_type_des
            )
            new_room_type.save()
        except:
            messages.info(request, 'Some information of room type provided is incorrect! Please check again')
            return redirect('/addroom')

        ##  Add bed information
        try:
            bed_size = [float(bedsize) for bedsize in  request.POST.getlist('bedsize')]
            bed_quantity = [int(bedquantity) for bedquantity in request.POST.getlist('bedquantity')]
        except:
            messages.info(request, 'Value error. Maybe you enter wrong format: Float: x.x not x,x')
            return redirect('/addroom')

        if len(bed_size) != len(set(bed_size)):
            messages.info(request, "Same bed size need to be defined in Bed quantity")
            return redirect('/addroom')

        try: 
            for idx, _size in enumerate(bed_size):
                Bedinfo.objects.create(
                    bed_typeid = new_room_type,
                    size = _size,
                    quantity = bed_quantity[idx]
                )
        except:
            messages.info(request, "Some errors occure in adding bed information. Please try again")
            return redirect('/addroom')

        ##  Check supply information
        try:
            supply_id_list = [int(supply_id) for supply_id in  request.POST.getlist('supply_id')]
            supply_quantity = [int(_quantity) for _quantity in request.POST.getlist('supply_quantity')]
        except:
            messages.info(request, 'Value error. Maybe you enter wrong format: Supply ID: Int & Quantity: Int')
            return redirect('/addroom')

        if len(supply_id_list) != len(set(supply_id_list)):
            messages.info(request, "Same supply id need to be defined in Supply quantity")
            return redirect('/addroom')
        try:
            for idx, sid in enumerate(supply_id_list):
                SupplyInRoom.objects.create (
                    sir_supplyid = sid,
                    sir_typeid = new_room_type,
                    num_supply = supply_quantity[idx]
                )
        except:
            messages.info(request, "Some errors occur in adding supply. Please try again")
            return redirect('/addroom')
    return render(request, 'addroom.html')