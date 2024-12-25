from django.contrib import admin
from django.urls import path, include
from django.shortcuts import HttpResponse, redirect
from django.shortcuts import render


def home(request):
    if not request.user.is_authenticated:
        return redirect("login")

    return render(request, 'home.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('stream/', include('stream.urls')),
]
