from django.shortcuts import render, redirect
from .models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse
from django.contrib.auth.models import User

# Create your views here.

def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, 'Usuário ou senha inválido')
    return redirect('/')

def cadastro_user(request):
    return render(request, 'cadastro-user.html')

def submit_cadastro_user(request):
    if request.POST:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if username is not None and email is not None and password is not None:
            User.objects.create_user(username=username,
                                    password=password,
                                    email=email)
            return redirect('/')
        else:
            messages.error(request, 'Preencha todos os campos')


@login_required(login_url='/login/')
def lista_eventos(request):
    usuario = request.user
    data_atual = datetime.now() - timedelta(hours=1)
    eventos = Evento.objects.filter(usuario=usuario,
                                    data_evento__gt=data_atual)
    context = {'eventos': eventos}
    return render(request, 'agenda.html', context)

@login_required(login_url='/login/')
def lista_historico_eventos(request):
    usuario = request.user
    eventos = Evento.objects.filter(usuario=usuario).order_by('data_evento')
    context = {'eventos': eventos}
    return render(request, 'historico.html', context)

@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    context = {}
    if id_evento:
        context['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', context)

@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        local = request.POST.get('local')
        id_evento = request.POST.get('id_evento')
        usuario = request.user
        if id_evento:
            Evento.objects.filter(id=id_evento).update(titulo=titulo,
                                                        data_evento=data_evento,
                                                        descricao=descricao,
                                                        usuario=usuario,
                                                        local=local)
        else:
            Evento.objects.create(titulo=titulo,
                                    data_evento=data_evento,
                                    descricao=descricao,
                                    usuario=usuario,
                                    local=local)
    return redirect('/')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404()
    return redirect('/')


def json_lista_evento(request, id_usuario):
    usuario = User.objects.get(id=id_usuario)
    eventos = Evento.objects.filter(usuario=usuario).values('id', 'titulo')
    return JsonResponse(list(eventos), safe=False)