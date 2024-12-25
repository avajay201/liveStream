from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.http import StreamingHttpResponse
from django import forms
import cv2
from .models import Stream
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


class StreamForm(forms.Form):
    title = forms.CharField(max_length=100, required=True, label="Stream Title")

def generate_frames():
    camera = cv2.VideoCapture(0)

    while True:
        ret, frame = camera.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            break
        
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

    camera.release()

def live_stream(request):
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

def start_stream(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if not request.user.is_superuser:
        messages.error(request, "You are not a authorized user to start a stream!")
        return redirect('home')

    if request.method == 'POST':
        form = StreamForm(request.POST)
        if form.is_valid():
            camera = cv2.VideoCapture(0)
            if not camera.isOpened():
                messages.error(request, "Unable to open the camera.")
                return redirect('home')
            title = form.cleaned_data['title']
            stream, _ = Stream.objects.get_or_create(title=title)
            print('stream.unique_key>>>', stream.unique_key)
            return render(request, 'stream/live_stream.html', {'title': stream.title, 'room_id': stream.unique_key, 'user': request.user.username})
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

    return render(request, 'stream/live_stream.html', {'title': stream.title, 'room_id': stream.unique_key, 'user': request.user.username})

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
    return render(request, "login.html")


def chat_room(request, room_name):
    return render(request, 'chat.html', {
        'room_name': room_name
    })

def logout_view(request):
    logout(request)
    return redirect("login")