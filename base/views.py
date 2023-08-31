from django.shortcuts import render, redirect

#it is for search - So person name, room name, topic name can be searched
from django.db.models import Q

from django.http import HttpResponse
from .models import Room, Topic

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import RoomForm

# rooms = [
#     {'id':1,'name':'Lets learn python!'},
#     {'id':2,'name':'Front end lesson'},
#     {'id':3, 'name':'Backend Lesson'}
# ]

#have function login - it s method so itll create problem
def LoginPage(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username = username, password= password)

        if user is not None:
            #adding session to db
            login(request, user)
            return redirect ('home')
        else:
            messages.error(request,'Username or password does not exist')
    context = {}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def home(request):
    # string q is equal to the what we pass it in the url
    q = request.GET.get('q') if request.GET.get('q') != None else ''

        # with the foreign key connection we go to the topic model and filter name
        # if icontains has filter value it ll use, not - then no
        # Q is for the searching by 3 different values 
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q)
                                )

    # rooms = Room.objects.all()
    
    #need to change topics for most viewed or smth
    topics= Topic.objects.all()

    #this works faster than python len
    room_count = rooms.count()


    context = {'rooms':rooms, 'topics':topics, "room_count": room_count}
    return render(request, 'base/home.html', context)


def room (request,pk):
    room = Room.objects.get(id = pk)
    context = {'room':room}
    return render(request, 'base/room.html', context)

def create_room (request):
    form = RoomForm()
    
    if request.method == "POST":
        print(request.POST)
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/room_form.html', context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)

    #prefilled with the room value that we bring with pk
    form = RoomForm(instance=room)

    if request.method == "POST":
        form = RoomForm(request.POST, instance = room) #this tells which room to update, any other case it ll create new one)
        if form.is_valid():
            form.save()
            return redirect('home')
        

    context = {'form':form}
    return render(request, 'base/room_form.html', context)


def deleteRoom(request,pk):
    room = Room.objects.get(id = pk)

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': room})


