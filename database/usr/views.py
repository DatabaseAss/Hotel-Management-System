from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, CustomManager
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        #Verify information
        if len(username) == 0 or len(password) == 0:
            messages.info(request, "Username and Password cannot be empty!")
            return redirect ('/login')

        try:
            user = CustomUser.objects.get(username = username)
        except:
            messages.info(request, "Username does not exist")
            return ('/login')

        user = authenticate(request, username = username, password = password)
        
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Incorrect Password, Try again.")
            return redirect('/login')
    return render(request, 'login.html')

def logoutUser(request):
    
    # logout(request)

    return redirect(request, '/login')

def registerUser(request):
    if request.method == "POST":
        full_name = request.POST['yourname']
        username = request.POST['username']
        password = request.POST['password']
        repassword = request.POST['repassword']
        #Verify no field empty
        if len(full_name) == 0 or len(username) == 0 or len(password) == 0 or len (repassword) == 0:
            messages.info(request, "You must fill in all information")
            return redirect('/register')
            
        if password != repassword:
            messages.info(request, "Password does not match")
        elif CustomUser.objects.filter(username = username).exists():
            messages.info(request, "Username had been already taken")
            return redirect ('/register')
        else: 
            #Create new user
            user = CustomUser.objects.create_user(fullname = full_name, username = username, password = password)
            user.save()
            login(request, user, backend='django.contrib.auth.backend.ModelBackend')
            return redirect('/login')
    return render(request, 'register.html')

