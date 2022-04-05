from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.messages import constants

def cadastro(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        if not password == confirm_password:
            messages.add_message(request, constants.ERROR, 'As senhas não são iguais!')
            return redirect('/auth/cadastro/')

        if len(username.strip()) == 0 or len(password.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Username e senhas não podem ficar vazios!')
            return redirect('/auth/cadastro/')

        user = User.objects.filter(username=username)

        if user.exists():
            messages.add_message(request, constants.ERROR, 'Usuário já existe!')
            return redirect('/auth/cadastro/')

        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return redirect('/auth/login/')

        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema!')
            return redirect('/auth/cadastro/')


def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        #vai no banco e ve se tem um user com essa senha
        user = auth.authenticate(username=username, password=password)

        if not user:
            messages.add_message(request, constants.ERROR, 'Username ou senha inválidos')
            return redirect('/auth/login/')
        else:
            auth.login(request, user)
            return redirect('/')


def logout(request):
    auth.logout(request)
    return redirect('/auth/login')
