from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Content(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField(Tag)
    header = models.CharField(max_length=200)
    link = models.URLField(null=True)
    # null --> for allowing empty values (in database)
    # blank --> for submitting forms with empty values
    description = models.TextField(null=True, blank=True)
    # participants =
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    PUBLIC = 'public'
    SHARED = 'shared'
    PRIVATE = 'private'
    VISIBILITY_CHOICES = [
        (PUBLIC, 'Public'),
        (SHARED, 'Shared'),
        (PRIVATE, 'Private'),
    ]
    visibility = models.CharField(
        max_length=7,
        choices=VISIBILITY_CHOICES,
        default=PUBLIC,
    )

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.header


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]
