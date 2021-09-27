from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from .models import *
from .forms import DocumentForm, FileForm

# Create your views here.
def main(request):
    return render(request,'mail/massages.html')

class Mail(View):
    def get(self, request):
        type_m=request.GET.get('type', 'inbox')
        user = User.objects.get(username=request.user)
        messages=[]
        if type_m == 'inbox':
            messages = Message.objects.filter(receiver=user)
        elif type_m == 'sent':
            messages = Message.objects.filter(sender=user)
        elif type_m == 'draft':
            messages = Message.objects.filter(draft=True)
        return render(request,'mail/messages.html',context={"messages":messages.order_by("-date"),"type_m":type_m})
    
    def post(self,request):
        pass

class MessageDetailView(DetailView):
    model = Message


class Compose(View):
    def get(self, request):
        fileform = FileForm()
        mform = DocumentForm()
        return render(request,'mail/compose.html',context={"fileform":fileform,"mform":mform})

    def post(self, request):
        data = request.POST.copy()
        fileform = FileForm(request.POST, request.FILES)
        receiver = User.objects.filter(username = request.POST['receiver']).first()
        if receiver:
            data.update({"receiver":receiver.id})
        else:
            data.update({"draft":True})
        form = DocumentForm(data, request.FILES)
        sender = User.objects.filter(username=request.user).first()
        form.instance.sender = sender
        if form.is_valid():
            message = form.save()
            files = request.FILES.getlist('file')
            if fileform.is_valid():
                for f in files:
                    file = File.objects.create(file=f)
                    #File.file.url (get path)
                    #code (path: media/encrypt_doc/fjisdjf.bin)
                    message.files.add(file)
                message.save()
            return redirect("messages")
        else:
            return render(request,'mail/compose.html',context={"fileform":fileform,"mform":form})