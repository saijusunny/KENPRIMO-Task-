from django.shortcuts import render, redirect
from .models import *
from  django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import os
from django.contrib.auth.models import User,auth
from datetime import datetime,date


# Create your views here.def 
from django.http import JsonResponse

def login(request):
    return render(request,'login.html')
def signup(request):
    
    return render(request, 'signup.html')



def usercreate(request):
    if request.method=="POST":
        fname=request.POST['first_name']
        lname=request.POST['last_name']
        username=request.POST['username']
        password=request.POST['password']
        cpass=request.POST['cpassword']
        email=request.POST['email']
      
        if password != cpass:
            messages.info(request, 'Passwords do not match!!!!!')
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already exists')
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email already exists')
            return redirect('signup')
        
        user=User.objects.create_user(
            first_name=fname,
            last_name=lname,
            username=username,
            password=password,
            email=email,
            
        )
        user.save()
        auth.login(request,user) 
        return redirect('home')

        
    else:
        return redirect('signup')


def adminlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        
        user = authenticate(request,username=username,password=password)
        
        if user is not None:
            if user.is_active:
                auth.login(request,user) 
                return redirect('home')
            else:
                return redirect('login')
                
        else:
            messages.info(request, 'invalid username and password, try again')
            return redirect('login')
    else:
        return redirect('login')

def logout_view(request):
    logout(request)
    return redirect('login') 

@login_required
def home(request):
    cat=RoomCategory.objects.all()
    return render(request, "home.html", {'cat':cat})

######################################################################-{CATEGORY}
def add_category(request):
    if request.method == "POST":
       
        addcat=RoomCategory()
        addcat.name=request.POST.get('category_name')
        addcat.base_price=request.POST.get('category_price')
        addcat.save()

    return redirect('view_category')
    
def view_category(request):
    cat= RoomCategory.objects.all()
    
    return render(request, "category/view_category.html", {'cat':cat})
    
def edit_category(request,id):
    cat=RoomCategory.objects.get(id=id)
    cat.name=request.POST.get('category_name')
    cat.base_price=request.POST.get('category_price')
    cat.save()
    return redirect('view_category')
    
def delete_category(request,id):
    cat=RoomCategory.objects.get(id=id)
    cat.delete()
    return redirect('view_category')

##########################################################################-{Room}
def add_room(request):
    if request.method == "POST":
        ids=request.POST.get('category')
        print(ids)
        cat=RoomCategory.objects.get(id=ids)
        addroom=Room()
        addroom.room_number=request.POST.get('room')
        addroom.category=cat
        addroom.is_available=request.POST.get('status')
        addroom.save()
    return redirect('view_room')

def view_room(request):
    rooms= Room.objects.all()
    cat=RoomCategory.objects.all()
    return render(request, "room/view_room.html", {'rooms':rooms, 'cat':cat})

def available_room(request):
    rooms= Room.objects.filter(is_available = 0)
    cat=RoomCategory.objects.all()
    return render(request, "room/view_room.html", {'rooms':rooms, 'cat':cat})

def edit_room(request,id):
    ids=request.POST.get('category')
    cat=RoomCategory.objects.get(id=ids)
    addroom=Room.objects.get(id=id)
  
    addroom.category=cat
    addroom.is_available=request.POST.get('status')
    addroom.save()
    return redirect('view_room')
    
def delete_room(request,id):
    cat=Room.objects.get(id=id)
    cat.delete()
    return redirect('view_room')
        

#########################################################################-{SpecialRate}

def add_specialrate(request):
    if request.method == "POST":
        ids=request.POST.get('category')
        print(ids)
        cat=RoomCategory.objects.get(id=ids)
        addspec=SpecialRate()
        
        addspec.room_category=cat.name
        addspec.start_date=request.POST.get('st_dt')
        addspec.end_date=request.POST.get('end_dt')
        addspec.room_multiplier=request.POST.get('price')
        addspec.save()
    return redirect('view_offer')
    
def view_offer(request):
    spcl= SpecialRate.objects.all()
    cat=RoomCategory.objects.all()
    return render(request, "Special_rate/view_offer.html", {'spcl':spcl, 'cat':cat})

def edit_specialrate(request,id):
    if request.method == "POST":
        addspec=SpecialRate.objects.get(id=id)
        addspec.room_category=request.POST.get('category')
        addspec.start_date=request.POST.get('st_dt')
        addspec.end_date=request.POST.get('end_dt')
        addspec.room_multiplier=request.POST.get('price')
        addspec.save()
    return redirect('view_offer')
    
def delete_specialrate(request,id):
    cat=SpecialRate.objects.get(id=id)
    cat.delete()
    return redirect('view_offer')
    
####################################################################### -{Reservation}
def reservation_home(request):
    cat=RoomCategory.objects.all()
    return render(request, "reservation/reservation_home.html", {'cat':cat})
    
def get_room(request):
    key=request.GET.get('cat')
    cats=RoomCategory.objects.get(id=key)
    dt=date.today()
   
    offer=SpecialRate.objects.filter(room_category=cats.name, start_date__gte=date.today()).last()
    print(offer.room_multiplier)
    rooms=Room.objects.filter(category=cats, is_available=0)
    rooms_data = [{'id': room.id, 'name': room.room_number} for room in rooms]
    data={
        'status': 'success',
        'rooms':rooms_data,
        'cat_price':cats.base_price,
        'off_pr':offer.room_multiplier,
    }
    return JsonResponse(data)

def room_reservation(request):
    if request.method == "POST":
        res=Reservation()
        res.user = request.user
        res.room =request.POST.get('room') 
        res.start_date=request.POST.get('start_date') 
        res.end_date=request.POST.get('end_date') 
        res.customer_name = request.POST.get('customer_name') 
        res.total_price = request.POST.get('total_amout') 
        res.save()
        return redirect('reservation_view')
    return redirect('reservation_view')

def reservation_view(request):
    res=Reservation.objects.filter(user=request.user)
    print(res)
    return render(request, "reservation/reservation_view.html", {'res':res})
