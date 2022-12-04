from django.contrib import admin

# Register your models here.
from .models import Content, Tag, Message

admin.site.register(Content)
admin.site.register(Tag)
admin.site.register(Message)
