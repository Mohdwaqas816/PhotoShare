from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from .models import Category, Photo
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.


def loginUser(request):
    page = 'login'

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('gallery')
        else:
            messages.error(request, 'Username OR password incorrect!')
            return redirect('login')
    

    
    return render(request, 'photos/login_register.html', {'page':page})


def logoutUser(request):
    logout(request)
    return redirect('login')




def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
           user =  form.save()
           login(request, user)
           messages.success(request, 'Registration Successful!')

           subject = 'Welconme to photoShare website!!'
           message = '''Thankyou for registring into our website. You can upload photos here and download whenever you need, Hope you will enjoy.
           Cc:PhotoShare team.'''
           send_mail(
               subject,
               message,
               settings.EMAIL_HOST_USER,
               [user.email],
               fail_silently=False,

           )
           return redirect('gallery')
        #    user.save()
        messages.error(request, 'User for this name already exist!')
        return redirect('register')


        #    user = authenticate(request, username=user.username, password=request.POST['password1'])

        #    if user is not None:
        #        login(request, user)
        #        return redirect('gallery')


           
            


    context = {'form':form, 'page':page}
    return render(request, 'photos/login_register.html', context)




@login_required(login_url='login')
def gallery(request):
    user = request.user

    category = request.GET.get('category')

    if category == None:
        photos = Photo.objects.filter(category__user=user)

    else:
        photos = Photo.objects.filter(category__name=category, category__user=user)


    categories = Category.objects.filter(user=user)

    context = {'categories':categories, 'photos':photos}

    return render(request, 'photos/gallery.html', context)


@login_required(login_url='login')
def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)

    context = {'photo':photo}
    return render(request, 'photos/photo.html', context)


@login_required(login_url='login')
def addPhoto(request):
    user = request.user
    categories = user.category_set.all()

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])

        elif data['category_new'] != '':
            category, create = Category.objects.get_or_create(user=user, name=data['category_new'])
        else:
            category = None
        for image in images:
            photo = Photo.objects.create(category=category, description=data['description'], image=image)
        return redirect('gallery')

    context = {'categories':categories}
    return render(request, 'photos/add.html', context)