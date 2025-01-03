from django.shortcuts import render, redirect
from django import forms
from .models import Stream
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


class StreamForm(forms.Form):
    title = forms.CharField(max_length=100, required=True, label="Stream Title")

def start_stream(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if not request.user.is_superuser:
        messages.error(request, "You are not a authorized user to start a stream!")
        return redirect('home')

    if request.method == 'POST':
        form = StreamForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            stream, _ = Stream.objects.get_or_create(title=title, created_by=request.user)
            return render(request, 'stream/live_stream.html', {'stream': stream})
    else:
        form = StreamForm()

    return render(request, 'stream/start_stream.html', {'form': form})

def join_stream(request):
    if not request.user.is_authenticated:
        return redirect("login")

    id = request.POST.get('stream_id')
    if not id:
        messages.error(request, "Stream ID not found!")
        return redirect('home')

    stream = Stream.objects.filter(unique_key=id).first()

    if not stream:
        messages.error(request, "Stream does not exists!")
        return redirect('home')
    return render(request, 'stream/live_stream.html', {'stream': stream})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        messages.error(request, "Invalid credentials!")
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def close_stream(request, key):
    stream = Stream.objects.filter(unique_key=key).first()
    if not stream:
        messages.error(request, "Stream does not exists!")
        return redirect("home")
    stream.delete()
    return redirect("home")
