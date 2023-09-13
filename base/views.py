from django.shortcuts import render, redirect

#it is for search - So person name, room name, topic name can be searched
from django.db.models import Q

#for page restrict to notusers
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from .models import Room, Topic, Message

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

#for registration form
from django.contrib.auth.forms import UserCreationForm


from .forms import RoomForm

# rooms = [
#     {'id':1,'name':'Lets learn python!'},
#     {'id':2,'name':'Front end lesson'},
#     {'id':3, 'name':'Backend Lesson'}
# ]

#have function login - it s method so itll create problem
def LoginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect ('home')

    if request.POST:
        username = request.POST.get('username').lower()
        
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
    context = {'page':page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page = 'register'
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            #it will save user data but will not commit it to the db so we will lowercase username in order not to face with problem
            user = form.save(commit =False)
            user.username = user.username.lower() #make it lowercase
            user.save()    

            #login user directly after registration 
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')


        


    context = {'page':page,'form':form}
    return render(request,'base/login_register.html',context)



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

    #show activity in Recent Activity section
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q)).order_by('-updated')



    context = {'rooms':rooms, 'topics':topics, "room_count": room_count,'room_messages':room_messages}
    return render(request, 'base/home.html', context)


def room (request,pk):
    room = Room.objects.get(id = pk)

    #we can query child objects of specific 
    #message_set>
    #  message is the model name we can write it lowercase and add set
    # all> means get all related child rows
    #order by is for latest messages "-"" means descending
    room_messages = room.message_set.all().order_by('-created')
    
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )

        #it adds user to the room if someone writes the message in the room
        room.participants.add(request.user)


        #even without this return function it will work and after post u ll see message BUT
        # it can create some problems afterwards considering POST method will keep data - so need to fully refresh it
        return redirect('room',pk = room.id)


    context = {'room':room, 'room_messages':room_messages,'participants' : participants}
    return render(request, 'base/room.html', context)


@login_required
def userProfile(request, pk):
    user = User.objects.get(id = pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()


    context = {'user':user, 'rooms':rooms,
               'room_messages':room_messages, 'topics':topics}
    return render(request, 'base/profile.html', context)



@login_required(login_url = "login")
def create_room (request):
    form = RoomForm()
    
    if request.method == "POST":
        print(request.POST)
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit =False)

            #which user creates the room will be the host automatically
            room.host = request.user
            room.save()


            return redirect('home')

    context = {'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url = "login")
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)


    #login restriction is also require this action in case of someone knows the url eventhough not logged in
    if request.user != room.host:
        return HttpResponse ('You are not allowed here!!')


    #prefilled with the room value that we bring with pk
    form = RoomForm(instance=room)

    if request.method == "POST":
        form = RoomForm(request.POST, instance = room) #this tells which room to update, any other case it ll create new one)
        if form.is_valid():
            form.save()
            return redirect('home')
        

    context = {'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url = "login")
def deleteRoom(request,pk):
    room = Room.objects.get(id = pk)

        #login restriction is also require this action in case of someone knows the url eventhough not logged in
    if request.user != room.host:
        return HttpResponse ('You are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url = "login")
def deleteMessage(request,pk):
    message = Message.objects.get(id = pk)

        #login restriction is also require this action in case of someone knows the url eventhough not logged in
    if request.user != message.user:
        return HttpResponse ('You are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': message})




