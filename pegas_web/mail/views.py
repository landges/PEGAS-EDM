from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from .models import *
from passport.models import *
from .forms import DocumentForm, FileForm
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

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

class MessageDetailView(View):
    def get(self,request,pk):
        message=Message.objects.get(id=pk)
        username = message.sender.username
        files = message.files.all()
        public_key = Center.objects.using('center').filter(user = username).first().public_key
        valid = True
        valid_dict = {}
        for file in files:
            content = file.file.read()
            hash_doc = "b'"+hashlib.md5(bytes(content)).hexdigest()+"'"
            key = RSA.import_key(public_key)
            cipher_rsa = PKCS1_OAEP.new(key)
            hash_check = cipher_rsa.decrypt(file.encrypt_hash)
            if str(hash_check) != hash_doc: 
                valid_dict[file]='False'
            else:
                valid_dict[file]='True'
        print(valid_dict)     
        return render(request,'mail/message_detail.html',context={'message':message,"valid_dict":valid_dict, 'valid': valid})

    def post(self,request):
        pass


class Compose(View):
    def get(self, request):
        fileform = FileForm()
        mform = DocumentForm()
        return render(request,'mail/compose.html',context={"fileform":fileform,"mform":mform})

    def post(self, request):
        data = request.POST.copy()
        print(data)
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
                    data = f.read()
                    hash_file = hashlib.md5(bytes(data)).hexdigest()
                    private_key = sender.profile.private_key
                    key = RSA.import_key(private_key)
                    cipher_rsa = PKCS1_OAEP.new(key)
                    ciphertext = cipher_rsa.encrypt(bytearray(hash_file, encoding='utf-8'))
                    file = File.objects.create(file=f, encrypt_hash=ciphertext)
                    message.files.add(file)
                message.save()
            return redirect("messages")
        else:
            return render(request,'mail/compose.html',context={"fileform":fileform,"mform":form})

class Create_Route(View):
    def get(self, request):
        fileform = FileForm()
        mform = DocumentForm()
        return render(request,'mail/create_route.html',context={"fileform":fileform,"mform":mform})

    def post(self, request):
        data = request.POST.copy()
        print(data)
        # fileform = FileForm(request.POST, request.FILES)
        # receiver = User.objects.filter(username = request.POST['receiver']).first()
        # if receiver:
        #     data.update({"receiver":receiver.id})
        # else:
        #     data.update({"draft":True})
        # form = DocumentForm(data, request.FILES)
        # sender = User.objects.filter(username=request.user).first()
        # form.instance.sender = sender
        # if form.is_valid():
        #     message = form.save()
        #     files = request.FILES.getlist('file')
        #     if fileform.is_valid():
        #         for f in files:
        #             file = File.objects.create(file=f)
        #             message.files.add(file)
        #         message.save()
        #     return redirect("messages")
        # else:
        #     return render(request,'mail/create_route.html',context={"fileform":fileform,"mform":form})