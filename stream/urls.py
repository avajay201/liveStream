from django.urls import path
from .views import start_stream, join_stream, login_view,chat_room, logout_view

urlpatterns = [
    path('start-stream/', start_stream, name='start-stream'),
    path('join-stream/', join_stream, name='join-stream'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('chat/<str:room_name>/', chat_room, name='chat_room'),
]
