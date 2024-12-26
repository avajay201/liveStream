from django.urls import path
from .views import start_stream, join_stream, login_view, logout_view, close_stream

urlpatterns = [
    path('start-stream/', start_stream, name='start-stream'),
    path('join-stream/', join_stream, name='join-stream'),
    path('close-stream/<key>', close_stream, name='close-stream'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
