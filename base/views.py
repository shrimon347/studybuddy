from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import MyUserCreationForm, RoomForm, UserForm
from .models import Message, Room, Topic, User


# Create your views here.



def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('note')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('note')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('note')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('note')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})



#this is room data bois.
def rooms(request):  

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.all()[0:5]
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))[0:3]
    # pagination 
    RoomData = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    room_count = RoomData.count()
    page = Paginator(RoomData, 5)
    page_number = request.GET.get('page', 1)
    roomDataFinal = page.get_page(page_number)
    totalpage = roomDataFinal.paginator.num_pages

    context = {'topics': topics,'room_count': room_count, 'room_messages': room_messages, 'roomdata':roomDataFinal, 'lastpage':totalpage,'totalpagelist':[n+1 for n in range (totalpage)],'page':page_number}
    return render(request, 'base/rooms.html', context)

@login_required(login_url='login')
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'base/room.html', context)




@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('rooms')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('rooms')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('rooms')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('rooms')
    return render(request, 'base/delete.html', {'obj': message})

def userProfile(request, username):
    user = User.objects.get(username=username)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    posts = user.post_set.all()
    topics = Topic.objects.all()
    page = Paginator(rooms, 5)
    page_number = request.GET.get('page',1)
    roomDataFinal = page.get_page(page_number)
    totalpage = roomDataFinal.paginator.num_pages
    
            
    context = {'user': user, 'roomdata': roomDataFinal, "posts":posts,
               'room_messages': room_messages,'topics': topics,'lastpage':totalpage,'totalpagelist':[n+1 for n in range (totalpage)],'page':page_number}
    return render(request, 'base/profile.html', context)
   
@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', username=user.username)

    return render(request, 'base/update-user.html', {'form': form})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})


    