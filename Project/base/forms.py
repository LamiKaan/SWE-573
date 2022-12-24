from django.forms import ModelForm
from django.forms import CharField
from .models import Content, Profile

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic']
        # fields = '__all__'


class ContentForm(ModelForm):
    tag = CharField(required=False,
                    help_text='<br/>You can enter multiple tags by separating them with commas(,).')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in ['header', 'link', 'description', 'visibility']:
            self.fields[field_name].help_text = None

        self.fields['link'].required = False

        # self.fields[
        #     'tag'].help_text = '<br/>You can enter multiple tags by separating them with commas(,).'

        self.fields["header"].widget.attrs.update({
            'required': '',
            # 'name': 'username',
            # 'id': 'username',
            # 'type': 'text',
            # 'class': 'form-input',
            # 'placeholder': 'Username',
            # 'maxlength': '50',
            # 'minlength': '1'
        })

        # self.fields["tag"].widget.attrs.update({
        #     'required': '',
        #     'name': 'username',
        #     'id': 'username',
        #     'type': 'char',
        #     'class': 'form-input',
        #     'placeholder': 'tags',
        #     'maxlength': '50',
        #     'minlength': '1'
        # })

        # self.fields["link"].widget.attrs.update({
        # 'required': '',
        #     'name': 'username',
        #     'id': 'username',
        #     'type': 'text',
        #     'class': 'form-input',
        #     'placeholder': 'Username',
        #     'maxlength': '50',
        #     'minlength': '1'
        # })

        # self.fields["description"].widget.attrs.update({
        #     'required': '',
        #     'name': 'username',
        #     'id': 'username',
        #     'type': 'text',
        #     'class': 'form-input',
        #     'placeholder': 'Username',
        #     'maxlength': '50',
        #     'minlength': '1'
        # })

    class Meta:
        model = Content
        # fields = ['owner', 'header', 'description']
        fields = ['header', 'tag', 'link', 'description', 'visibility']
        # widgets = {
        #     'tag': CharField(),
        # }


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in ['username', 'email', 'password1', 'password2']:
            self.fields[field_name].help_text = None

        self.fields["username"].widget.attrs.update({
            'required': '',
            'name': 'username',
            'id': 'username',
            'type': 'text',
            'class': 'form-input',
            'placeholder': 'Username',
            'maxlength': '50',
            'minlength': '1'
        })

        self.fields["email"].widget.attrs.update({
            'required': '',
            'name': 'email',
            'id': 'email',
            'type': 'text',
            'class': 'form-input',
            'placeholder': 'email@address.com'
        })

        self.fields["password1"].widget.attrs.update({
            'required': '',
            'name': 'password1',
            'id': 'password1',
            'type': 'text',
            'class': 'form-input',
            'placeholder': 'password',
            'maxlength': '50',
            'minlength': '1'
        })

        self.fields["password2"].widget.attrs.update({
            'required': '',
            'name': 'password2',
            'id': 'password2',
            'type': 'text',
            'class': 'form-input',
            'placeholder': 'password',
            'maxlength': '50',
            'minlength': '1'
        })

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
