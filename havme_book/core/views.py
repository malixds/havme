from itertools import chain
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    # user_item = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    
    # user_posts = Post.objects.filter(user=pk)
    # user_post_length = len(user_posts)
    # posts = Post.objects.all()
    context ={
        # 'user_item': user_item,
        'user_profile': user_profile,
        # 'posts': posts,
        # 'user_posts': user_posts,
        # 'user_post_length': user_post_length,
    }
    return render(request, 'index.html', context)




# @login_required(login_url='signin')
# def upload(request):

#     if request.method == "POST":
#         user = request.user.username
#         message = request.POST['message']

#         new_post = Post.objects.create(user=user, message=message)
#         new_post.save()

#     else:
#         return redirect('home')

@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == "POST":
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)
        
        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list))

    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})

def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == "POST":

        if request.FILES.get('images') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            first_name = request.POST['first_name']
            second_name = request.POST['second_name']
            age = request.POST['age']
            city = request.POST['city']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.city = city
            user_profile.first_name = first_name
            user_profile.second_name = second_name
            user_profile.age = age
            user_profile.save()

        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            first_name = request.POST['first_name']
            second_name = request.POST['second_name']
            age = request.POST['age']
            city = request.POST['city']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.city = city
            user_profile.first_name = first_name
            user_profile.second_name = second_name
            user_profile.age = age
            user_profile.save()
        
        return redirect('settings')

    return render(request, 'settings.html', {'user_profile': user_profile})

def signup(request):

    if request.method == 'POST':    #если запрос POST
        username = request.POST['username'] #username = значению, которое ввел пользователь
        email = request.POST['email']       # аналогично
        password = request.POST['password'] # аналогично
        password2 = request.POST['password2']   # аналогично

        if password == password2:   # если пароли введены одинаковые то :
            if User.objects.filter(email=email).exists():   # проеврка на суещствоваение профиля с таким же email'ом
                messages.info(request, 'Email Taken')       # отправляем сообщение о том, что такой email занят
                return redirect('signup')                   # перенаправляем пользователя на signup
            elif User.objects.filter(username=username).exists():   # проверка на суещствование пользователя с таким же никнеймом
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:   # если все ок, то:
                user = User.objects.create_user(username=username, email=email, password=password)  # создаем полльзователя с определенными данными
                user.save() # сохраняем его в базу данных

                """
                    Log user in and redirect to setting page / Заходим в пользователя -> и переходим на страницу с настройками
                """
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)    # user_model - ник пользовател 
                new_profile = Profile.objects.create(user=user_model, id_user = user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
    else:
        return render(request, 'signup.html')
    
def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password = password)

        if user is not None:
            auth.login(request, user)
            return redirect('settings')
        else:
            messages.info(request, 'Credent Invalid')
            return redirect('signin')
    else:
        return render(request, 'signin.html')
    

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

