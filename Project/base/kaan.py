# from models import Tag

# Topic.objects.all()

from django.db import models
from django.contrib.auth.models import User

from .models import Tag, Content, Message

for c in Content.objects.all():
    print(c.header)

print('Berk')
print('Degerli')
