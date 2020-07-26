from django.shortcuts import render, redirect
from .models import Evento

# Create your views here.
# def index(request):
#     return redirect('/agenda/')

def lista_eventos(request):
    usuario = request.user
    eventos = Evento.objects.all()
    context = {'eventos': eventos}
    return render(request, 'agenda.html', context)