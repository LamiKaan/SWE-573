from django.forms import ModelForm
from django.forms import CharField
from .models import Content


class ContentForm(ModelForm):
    tag = CharField()

    class Meta:
        model = Content
        # fields = ['owner', 'header', 'description']
        fields = '__all__'
