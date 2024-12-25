from django.contrib import admin
from .models import Stream

@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ('title', 'unique_key')  # Fields to display in the admin list view
