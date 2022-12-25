from django.db import models
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError
# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Content(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    tag = models.ManyToManyField(Tag)
    header = models.CharField(max_length=200)
    link = models.URLField(null=True)
    # null --> for allowing empty values (in database)
    # blank --> for submitting forms with empty values
    description = models.TextField(null=True, blank=True)
    # participants =
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    likes = models.ManyToManyField(User, related_name='has_liked_objects')

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


class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(
        default='default_profile_pic.png', null=True, blank=True)

    def __str__(self):
        return self.owner.username


class Follow(models.Model):
    followee = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='followed_profiles')
    follower = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='following_profiles')

    def clean(self):
        if self.followee == self.follower:
            raise ValidationError("Users can't follow themselves")

        objects = Follow.objects.all().order_by('-pk')
        last_pk = objects[0].pk

        if Follow.objects.filter(followee=self.followee, follower=self.follower).exclude(pk=last_pk).count() > 0:
            raise ValidationError(
                "Can't create another follow with same users")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Follow, self).save(*args, **kwargs)

    def __str__(self):
        return 'Followed: ' + self.followee.owner.username + ' - Follower: ' + self.follower.owner.username
