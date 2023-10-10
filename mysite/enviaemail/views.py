from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
def envia_email(request):
    send_mail('Assunto','Este é o email que estou te enviando','denilsongustavoln@gmail.com',['denilsongustavoln@gmail.com'])
    return HttpResponse('Olá')