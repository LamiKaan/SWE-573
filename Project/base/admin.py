from django.contrib import admin

# Register your models here.
from .models import Content, Tag, Message, Profile

admin.site.register(Content)
admin.site.register(Tag)
admin.site.register(Message)
admin.site.register(Profile)
