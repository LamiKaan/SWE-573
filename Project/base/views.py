from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from .models import Tag, Content, Message
from .forms import ContentForm
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
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'base/login_register.html', {'form': form})


def content(request, pk):
    content = Content.objects.get(id=pk)
    context = {'content': content}
    return render(request, 'base/content.html', context)


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

    print(contents)

    content_count = contents.count()
    tags = Tag.objects.all()

    context = {'contentscontext': contents,
               'tagscontext': tags, 'content_count': content_count}
    return render(request, 'base/home.html', context)


@login_required(login_url='login')
def createContent(request: HttpRequest):
    # form = ContentForm()

    if request.method == 'POST':
        # print(request.POST)
        # form = ContentForm(request.POST)
        # if form.is_valid():
        #     form.save()
        #     return redirect('home')
        content_obj = Content.objects.create(header=request.POST['header'],
                                             description=request.POST['description'],
                                             owner=request.user)

        for tagname in request.POST['tag'].split(','):
            currenttag, _ = Tag.objects.get_or_create(name=tagname)
            content_obj.tag.add(currenttag)

        content_obj.save()
        return redirect('home')

    # context = {'form': form}

    return render(request, 'base/content_form.html')
    # return HttpResponse('Oto')


@login_required(login_url='login')
def updateContent(request, pk):
    content = Content.objects.get(id=pk)

    form = ContentForm(instance=content)

    if request.user != content.owner:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        form = ContentForm(request.POST, instance=content)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/content_form.html', context)


@login_required(login_url='login')
def deleteContent(request, pk):
    content = Content.objects.get(id=pk)

    if request.user != content.owner:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        content.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': content})
