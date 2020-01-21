from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import generic
import datetime
from base_user.models import MyUser
from .forms import UserRegisterForm, AddFile, LoginForm
from .models import File, See
from .mongo_client import Repo


# Create your views here.S
def index(request):
    context = {}
    file = File.objects.all()
    temp = []
    for i in file:
        # print(i,'++++++++++++++++++++++++++++++++')
        test = i.files.all()
        for j in test:
            if request.user == j.see_user:
                temp.append(j.see_file)

    # print(temp)
    context['file'] = temp

    return render(request, 'index.html', context)


def register(request):
    context = {}
    form = UserRegisterForm
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # print('formvalid')
            username = form.cleaned_data['username']
            user = form.save(commit=False)

            user.set_password(form.cleaned_data['password'])
            user.save()

        else:
            form = UserRegisterForm()
            # print('!!!!!!!!!!!!!!!!!!')
    context['form'] = form
    return render(request, 'register.html', context)


def user_login(request):
    context = {}

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    user_browser = request.user_agent.browser
                    user_os = request.user_agent.os
                    user_ip = request.META['REMOTE_ADDR']
                    Repo.save('user_about', {
                        'User_Browser': user_browser,
                        'User_OS': user_os,
                        'User_IP': user_ip
                    })

                    return redirect('index')
                else:
                    return redirect('/')
            else:
                return redirect('/')
    context['form'] = LoginForm()
    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def addfile(request):
    context = {}
    if request.method == "POST":
        form = AddFile(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            See.objects.create(see_user=article.user, see_file=article, access_comment=True)
            return redirect('index')

    context['form'] = AddFile()
    return render(request, 'addfile.html', context)


def Detail(request, id):
    context = {}
    temp = []
    mongo = Repo()
    comments=mongo.search('comments',{'file_id':id})
    file = File.objects.filter(id=id).last()
    comment_check = See.objects.filter(see_user=request.user, see_file=file)
    # print(file.files.all())
    obj = file.files.all()

    for j in obj:
        temp.append(j.see_user)
        if request.user == j.see_user:
            file_detail = j.see_file

    # print(temp)
    context['test'] = comment_check
    context['file'] = file_detail
    if request.method == "POST":
        user = request.POST.get("hi")
        comment = request.POST.get("comment")
        nocomment = request.POST.get("nocomment")
        my_user = MyUser.objects.filter(username=user).last()
        if my_user not in temp:
            if comment:
                See.objects.create(see_user=my_user, see_file=file, access_comment=True)
                messages.success(request, 'Ugurla elave olundu')

            elif nocomment:
                See.objects.create(see_user=my_user, see_file=file, access_nocomment=True)
                messages.success(request, 'Ugurla elave olundu')

    else:
        messages.error(request, 'Bele bir istifadeci yoxdur')

    return render(request, 'detail.html', context)
