from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from .models import Tag, Content, Message, Profile, Follow
from .forms import ContentForm, RegisterForm, ProfileForm
# Create your views here.

# rooms = [
#     {'id': 1, 'name': 'Lets learn python'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'Frontend developers'},
# ]


def loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.add_message(request, messages.INFO, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = user.email.lower()
            user.save()
            login(request, user)

            profile_obj = Profile.objects.create(owner=user)
            profile_obj.save()
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'base/register.html', {'form': form})


@login_required(login_url='login')
def content(request, pk):
    content = Content.objects.get(id=int(pk))
    pk_var = content.pk
    # print(content.likes)
    # print(content.likes.count())
    like_count = content.likes.count()

    if content.likes.filter(id=request.user.pk).exists():
        like_status = True
    else:
        like_status = False

    if request.method == 'POST' and 'Like' in request.POST:
        content.likes.add(request.user)

        return redirect('content', pk=pk_var)

    elif request.method == 'POST' and 'Unlike' in request.POST:
        content.likes.remove(request.user)

        return redirect('content', pk=pk_var)

    context = {'content': content, 'like_count': like_count,
               'like_status': like_status}
    return render(request, 'base/content.html', context)


@login_required(login_url='login')
def profile(request, pk):
    user = User.objects.get(id=int(pk))

    try:
        profile = Profile.objects.get(owner__id=int(pk))
    except:
        profile = Profile.objects.create(owner=user)
        profile.save()

    pk_var = str(profile.owner.pk)

    # print(profile)
    # print(type(profile))
    # print(profile.owner)
    # print(type(profile.owner))
    # print(profile)
    follow_objects = Follow.objects.filter(followee=profile)
    # print(type(follows))
    # print(follows)
    follower_users = []
    for follow in follow_objects:
        # print(follow.follower)
        follower_users.append(follow.follower.owner)
    # print(followers)
    # print(followers[0])
    follow_status = request.user in follower_users
    # print(follow_status)

    request_profile = Profile.objects.get(owner=request.user)

    if request.method == 'POST' and 'Follow' in request.POST:
        follow_obj = Follow.objects.create(
            followee=profile, follower=request_profile)
        follow_obj.save()

        return redirect('profile', pk=pk_var)
        # return redirect('home')

    elif request.method == 'POST' and 'Unfollow' in request.POST:
        follow_obj = Follow.objects.get(
            followee=profile, follower=request_profile)
        follow_obj.delete()

        # return redirect('profile', pk=pk_var)
        return redirect('home')

    context = {'profile': profile, 'follow_status': follow_status}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def editProfile(request, pk):
    profile = Profile.objects.get(owner__id=int(pk))

    if request.user != profile.owner:
        return HttpResponse('You are not allowed here!')

    form = ProfileForm(instance=profile)

    pk_var = str(profile.owner.pk)
    # print(pk_var)

    if request.method == 'POST' and 'Save' in request.POST:
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile.bio = form.cleaned_data['bio']
            profile.profile_pic = form.cleaned_data['profile_pic']
            profile.save()

            return redirect('profile', pk=pk_var)

    elif request.method == 'POST' and 'Cancel' in request.POST:

        return redirect('profile', pk=pk_var)

    context = {'form': form, 'value': 'Save', 'profile': profile}
    return render(request, 'base/profile_edit.html', context)


def home(request):
    # Benim kendi kendime denedigim
    '''
    q = request.GET.get('q')

    if q is None:
        rooms = Room.objects.all()
    else:
        rooms = Room.objects.filter(topic__name=q)
    '''
    # /home?q=asd&page_type=me&
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    page_type = request.GET.get('page_type')

    if page_type == 'me':
        contents = Content.objects.filter(owner=request.user)
    else:
        if q == None:
            contents = Content.objects.all()
        else:
            contents = Content.objects.filter(
                Q(tag__name__icontains=q) |
                Q(header__icontains=q) |
                Q(description__icontains=q)
            ).distinct()

    # print('Below are all the contents')
    # print()
    # print(contents)

    content_count = contents.count()
    tags = Tag.objects.all()

    print(request.session.keys())
    print(request.session.values())

    context = {'contentscontext': contents,
               'tagscontext': tags, 'content_count': content_count}
    return render(request, 'base/home.html', context)


@login_required(login_url='login')
def createContent(request: HttpRequest):
    form = ContentForm()

    if request.method == 'POST':
        form = ContentForm(request.POST)
        if form.is_valid():
            obj_owner = request.user
            obj_header = form.cleaned_data['header']
            obj_link = form.cleaned_data['link']
            obj_description = form.cleaned_data['description']
            obj_visibility = form.cleaned_data['visibility']

            content_obj = Content.objects.create(
                owner=obj_owner, header=obj_header, link=obj_link, description=obj_description, visibility=obj_visibility)

            for obj_tag in form.cleaned_data['tag'].replace(" ", "").split(','):
                obj_tag, _ = Tag.objects.get_or_create(name=obj_tag)
                content_obj.tag.add(obj_tag)

            content_obj.save()
            return redirect('home')

    # if request.method == 'POST':
    #     # print(request.POST)
    #     # form = ContentForm(request.POST)
    #     # if form.is_valid():
    #     #     form.save()
    #     #     return redirect('home')
    #     content_obj = Content.objects.create(header=request.POST['header'],
    #                                          description=request.POST['description'],
    #                                          owner=request.user)

    #     for tagname in request.POST['tag'].replace(" ", "").split(','):
    #         currenttag, _ = Tag.objects.get_or_create(name=tagname)
    #         content_obj.tag.add(currenttag)

    #     content_obj.save()
    #     return redirect('home')

    context = {'form': form, 'value': 'Create'}

    return render(request, 'base/content_form_2.html', context)
    # return HttpResponse('Oto')


@login_required(login_url='login')
def updateContent(request, pk):

    content = Content.objects.get(id=int(pk))

    if request.user != content.owner:
        return HttpResponse('You are not allowed here!')

    # print(content)
    content_tags = content.tag.all()
    tags_list = []
    for eachtag in content_tags:
        tags_list.append(eachtag.name)
    # print(tags_list)
    tags_str = ', '.join(tags_list)
    # print(tags_str)
    # print()
    # print(content_tags)
    # print(type(content_tags[0]))
    # print(content_tags[0].name)

    form = ContentForm(instance=content)
    form.initial['tag'] = tags_str

    if request.method == 'POST':
        # form = ContentForm(request.POST, instance=content)
        form = ContentForm(request.POST)
        if form.is_valid():
            content.header = form.cleaned_data['header']
            content.link = form.cleaned_data['link']
            content.description = form.cleaned_data['description']
            content.visibility = form.cleaned_data['visibility']

            for eachtag in content_tags:
                content.tag.remove(eachtag)

            for new_tag in form.cleaned_data['tag'].replace(" ", "").split(','):
                new_tag, _ = Tag.objects.get_or_create(name=new_tag)
                content.tag.add(new_tag)

            content.save()
            return redirect('home')

    context = {'form': form, 'value': 'Save'}
    return render(request, 'base/content_form_2.html', context)


@login_required(login_url='login')
def deleteContent(request, pk):
    content = Content.objects.get(id=pk)

    if request.user != content.owner:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        content.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': content})
