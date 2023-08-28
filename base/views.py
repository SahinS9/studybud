from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic
from .forms import RoomForm

# rooms = [
#     {'id':1,'name':'Lets learn python!'},
#     {'id':2,'name':'Front end lesson'},
#     {'id':3, 'name':'Backend Lesson'}
# ]



def home(request):
    # string q is equal to the what we pass it in the url
    q = request.GET.get('q') if request.GET.get('q') != None else ''

        # with the foreign key connection we go to the topic model and filter name
        # if icontains has filter value it ll use, not - then no
    rooms = Room.objects.filter(topic__name__icontains = q)

    # rooms = Room.objects.all()
    
    #need to change topics for most viewed or smth
    topics= Topic.objects.all()



    context = {'rooms':rooms, 'topics':topics}
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