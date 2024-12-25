from django.contrib import admin
from .models import Chat, Stream

@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ('title', 'unique_key')
    readonly_fields = ('unique_key',)

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('stream',)
    readonly_fields = ('created_at',)
