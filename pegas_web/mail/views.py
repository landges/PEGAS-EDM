from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from .models import *

# Create your views here.
def main(request):
    return render(request,'mail/massages.html')

class Mail(View):
    def get(self, request):
        user = User.objects.get(username=request.user)
        messages = Message.objects.filter(receiver=user)
        return render(request,'mail/messages.html',context={"messages":messages})
    
    def post(self,request):
        pass

class MessageDetailView(DetailView):
    model = Message