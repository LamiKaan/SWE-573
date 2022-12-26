from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
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
    pk_var = str(content.pk)
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

    elif request.method == 'POST' and 'submit-comment' in request.POST:
        new_comment = Message.objects.create(
            user=request.user, content=content, body=request.POST.get('comment-text'))
        new_comment.save()

        return redirect('content', pk=pk_var)

    comments = Message.objects.filter(content=content)

    if content.its_messages.all().exclude(user=content.owner).count() + content.likes.count() == 0:
        editable = 1
    else:
        editable = 0

    context = {'content': content, 'like_count': like_count,
               'like_status': like_status, 'comments': comments, 'editable': editable}
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
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    follow_back = Follow.objects.filter(
        followee=request_profile, follower=profile).exists()

    contents_all = Content.objects.filter(owner=profile.owner)
    if profile == request_profile:
        visible_contents = contents_all.order_by('-created')
    else:
        if follow_status and follow_back:
            visible_contents = contents_all.filter(
                visibility__in=['shared', 'public']).distinct().order_by('-created')
        else:
            visible_contents = contents_all.filter(
                visibility__in=['public']).distinct().order_by('-created')

    visible_contents_count = visible_contents.count()

    editable_contents = []
    for each_content in visible_contents:
        if each_content.its_messages.all().exclude(user=each_content.owner).count() + each_content.likes.count() == 0:
            editable_contents.append(each_content)

    context = {'profile': profile, 'follow_status': follow_status,
               'follow_back': follow_back, 'visible_contents': visible_contents, 'visible_contents_count': visible_contents_count, 'editable_contents': editable_contents}
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

    request.session['q'] = q

    if q == '':
        # Every content in the database based on search results
        contents = Content.objects.all().distinct()
    else:
        # Every content in the database based on search results
        contents = Content.objects.filter(
            Q(tag__name__icontains=q) |
            Q(header__icontains=q) |
            Q(description__icontains=q) |
            Q(link__icontains=q) |
            Q(owner__username__icontains=q)
        ).distinct()

    # 1- Contents of the logged in user (for 'My Contents' section)
    contents_my = contents.filter(
        owner=request.user).distinct().order_by('-created')

    # 2- Public and shared contents of the logged in user's friends (for 'Friends' Contents' section)
    # Find friends first (logged in user follows and they follow back)
    user = Profile.objects.get(owner=request.user).owner
    user_profile = Profile.objects.get(owner=user)

    # Find the users that logged in user follows
    user_is_follower = Follow.objects.filter(follower=user_profile)

    followed_profiles = []
    for follow in user_is_follower:
        followed_profiles.append(follow.followee)

    followed_users = []
    for profile in followed_profiles:
        followed_users.append(profile.owner)

    # Find the users that follow the logged in user
    user_is_followee = Follow.objects.filter(followee=user_profile)

    follower_profiles = []
    for follow in user_is_followee:
        follower_profiles.append(follow.follower)

    follower_users = []
    for profile in follower_profiles:
        follower_users.append(profile.owner)

    # Find common users between followed_users and follower_users (=friends)
    friend_users = [
        user for user in followed_users if user in follower_users]

    # Get public and shared contents of friends
    contents_friends = contents.filter(owner__in=friend_users,
                                       visibility__in=['shared', 'public']).distinct().order_by('-created')

    # 3- Public contents of all other users (that are visible to everyone)
    exclude_users = [*friend_users, user]
    contents_other = contents.all().exclude(
        owner__in=exclude_users).filter(visibility='public').distinct().order_by('-created')

    # 4- All visible contents to the currently logged in user
    contents_all = contents_my.union(
        contents_friends, contents_other).order_by('-created')

    contents_all_count = contents_all.count()
    tags = Tag.objects.all()

    editable_contents = []
    for each_content in contents_all:
        if each_content.its_messages.all().exclude(user=each_content.owner).count() + each_content.likes.count() == 0:
            editable_contents.append(each_content)

    # print()
    # print(request.session.keys())
    # print()
    # print(request.session.values())
    # print()

    activity_contents = contents_all.order_by('-created')[0:10]
    contents_all_list = [content for content in contents_all]
    activity_messages = Message.objects.filter(
        content__in=contents_all_list).order_by('-created')[0:10]

    activity_contents_list = [content for content in activity_contents]
    activity_messages_list = [message for message in activity_messages]

    activities = []
    while (len(activities) < 10):
        if len(activity_contents_list) > 0 and len(activity_messages_list) > 0:
            if activity_contents_list[0].created >= activity_messages_list[0].created:
                obj = activity_contents_list.pop(0)
                activities.append([obj, 'content'])
            else:
                obj = activity_messages_list.pop(0)
                activities.append([obj, 'message'])
        elif len(activity_contents_list) > 0:
            obj = activity_contents_list.pop(0)
            activities.append([obj, 'content'])
        elif len(activity_messages_list) > 0:
            obj = activity_messages_list.pop(0)
            activities.append([obj, 'message'])
        else:
            break

    # print(activity_contents)
    # print()
    # print(activity_messages)
    # print()
    # print(activity_contents[0], type(activity_contents[0]),
    #       activity_contents[0].created, type(activity_contents[0].created))
    # print()
    # print(activity_messages[0], type(activity_messages[0]),
    #       activity_messages[0].created, type(activity_messages[0].created))
    # print()
    # print(activity_messages[0].created < activity_contents[0].created)
    # print()
    # # activities = [[object, type]]
    # print()
    # print('ACTIVITIES')
    # for activity in activities:
    #     print()
    #     print(activity)
    # print(len(activities))
    # print()

    profile = Profile.objects.get(owner=request.user)

    context = {'contents_all': contents_all,
               'tags': tags, 'contents_all_count': contents_all_count, 'editable_contents': editable_contents, 'profile': profile, 'activities': activities}
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

    if content.its_messages.all().exclude(user=content.owner).count() + content.likes.count() > 0:
        return HttpResponse("You can't update a content that already has likes or comments from other users. You can only delete it.")

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
    content = Content.objects.get(id=int(pk))

    if request.user != content.owner:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        content.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': content})


@login_required(login_url='login')
def deleteMessage(request, pk):
    comment = Message.objects.get(id=int(pk))

    content_pk = str(comment.content.pk)

    if request.user != comment.user:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        comment.delete()
        return redirect('content', pk=content_pk)

    return render(request, 'base/delete.html', {'obj': comment})
