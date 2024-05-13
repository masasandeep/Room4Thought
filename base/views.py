from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Room,Topic,Message
from .forms import RoomsForm
def loginPage(request):
    page='loginuser'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method =='POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist.')
        user = authenticate(request,username=username,password=password)
        if user!=None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist.')
    context = {'page':page}
    return render(request,'base\login_register.html',context)
def logOut(request):
    logout(request)
    return redirect('home')
def registerUser(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'error occured during registration')
    context = {'forms':form}
    return render(request,'base\login_register.html',context)
def userprofile(request,pk):
    user = User.objects.get(id=pk)
    room = user.room_set.all()
    topics = Topic.objects.all()
    room_message = user.message_set.all()
    context = {'rooms':room,'topics':topics,'room_messages':room_message}
    return render(request,'base\profile.html',context)
def home(request):
    q = request.GET.get('q') if request.GET.get('q')!=None else ''
    room = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains = q) |
        Q(description__icontains=q)
        )
    topic = Topic.objects.all()
    room_count = room.count()
    room_messages = Message.objects.filter(room__topic__name__icontains=q)
    context = {'rooms':room,'topics':topic,'roomcount':room_count,'room_messages':room_messages}
    return render(request,'base/home.html',context)
def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method=='POST':
        Message.objects.create(
            user= request.user,
            room = room,
            body = request.POST.get('body'),
        )
        room.participants.add(request.user)
        return redirect('room',pk = room.id)
    context = {'rooms':room,'messages':room_messages,'participants':participants}
    return render(request,'base/rooms.html',context)
@login_required(login_url='login')
def createroom(request):
    form = RoomsForm()
    if request.method=='POST':
        form = RoomsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request,'base/roomform.html',{'forms':form})
@login_required(login_url='login')
def updateroom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomsForm(instance=room)
    if request.method=='POST':
        form = RoomsForm(request.POST,instance=room)
        if form.is_valid:
            form.save()
            return redirect('home')
    return render(request,'base/roomform.html',{'forms':form})
@login_required(login_url='login')
def deleteroom(request,pk):
    room= Room.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('home')
    context = {'obj':room}
    return render(request,'base/delete.html',context)
def deletemessage(request,pk):
    message = Message.objects.get(id=pk)
    if request.method=='POST':
        message.delete()
        return redirect('home')
    context = {'obj':message}
    return render(request,'base/delete.html',context)