from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from .models import *
from passport.models import *
from .forms import DocumentForm, FileForm, RoadForm
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

# Create your views here.
def main(request):
    if request.user.groups.filter(name="boss").exists():
        userisboss = True
    else:
        userisboss = False
    return render(request,'mail/massages.html', context={"userisboss":userisboss})

class Mail(View):
    def get(self, request):
        if request.user.groups.filter(name="boss").exists():
            userisboss = True
        else:
            userisboss = False
        type_m=request.GET.get('type', 'inbox')
        user = User.objects.get(username=request.user)
        messages=[]
        if type_m == 'inbox':
            messages = Message.objects.filter(receiver=user)
        elif type_m == 'sent':
            messages = Message.objects.filter(sender=user)
        elif type_m == 'draft':
            messages = Message.objects.filter(draft=True)
        return render(request,'mail/messages.html',context={"messages":messages.order_by("-date"),"type_m":type_m, "userisboss":userisboss})
    
    def post(self,request):
        pass

class MessageDetailView(View):
    def get(self,request,pk):
        fileform = FileForm()
        
        message=Message.objects.filter(id=pk)
        mform = DocumentForm(message.values()[0])
        message = message.first()
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
        id_route = RouteMessageJournal.objects.filter(message_id=message).first()
        if id_route is not None:
            lastuser = UserInRoute.objects.filter(route=id_route.route_id, prevus=request.user).first().nextus
            return render(request,'mail/message_detail.html',context={'message':message,
                "valid_dict":valid_dict,
                'valid': valid,
                "fileform":fileform,
                "mform":mform,
                "id_route":id_route.route_id.id,
                "last_user_in_route":lastuser})
        else:
           return render(request,'mail/message_detail.html',context={'message':message,
                "valid_dict":valid_dict,
                'valid': valid,
                "fileform":fileform,
                "mform":mform}) 

def nextsteproad(request):
    data = request.POST.copy()
    sender = User.objects.filter(username=request.user).first()
    route_id = request.POST.get('id_route')
    route = UserInRoute.objects.filter(route=Road.objects.get(id=route_id), prevus=sender).first()
    receiver = route.nextus
    t_or_f = message_in_route(request, sender, receiver)
    if t_or_f == False:
        return render(request,'mail/compose.html') 
    else:
        rmj = RouteMessageJournal(
            prev_user=sender,
            next_user=receiver,
            message_id=Message.objects.get(id=t_or_f),
            route_id=route.route)
        rmj.save()
    return redirect("messages")


class Compose(View):
    def get(self, request):
        fileform = FileForm()
        mform = DocumentForm()
        return render(request,'mail/compose.html',context={"fileform":fileform,"mform":mform})

    def post(self, request):
        sender = User.objects.filter(username=request.user).first()
        receiver = User.objects.filter(username = request.POST['receiver']).first()
        t_or_f = message_in_route(request, sender, receiver)
        if t_or_f == False:
            return render(request,'mail/compose.html') 
        else:
            return redirect("messages")

class Create_Route(View):
    def get(self, request):
        fileform = FileForm()
        mform = DocumentForm()
        rform = RoadForm()
        return render(request,'mail/create_route.html',context={"fileform":fileform,"mform":mform, "rform":rform})

    def post(self, request):
        data = request.POST.copy()
        user_list=request.POST.getlist('node[]')
        creator = User.objects.get(username=request.user)
        receiver = User.objects.filter(username=user_list[0]).first()
        user_pairs = list()
        for i in range(len(user_list)):
            pair = list()
            if i != len(user_list)-1:
                pair.append(user_list[i])
                pair.append(user_list[i+1])
            else:
                pair.append(user_list[i])
                pair.append(None)
            user_pairs.append(pair)
        road=Road(creator=creator)
        road.save()
        usinroute = UserInRoute(
                    route=road,
                    prevus=User.objects.get(username=request.user),
                    nextus=User.objects.get(username=user_pairs[0][0])
                    )
        usinroute.save()
        for i in range(len(user_pairs)):
            if user_pairs[i][1] is not None:
                usinroute = UserInRoute(
                    route=road,
                    prevus=User.objects.get(username=user_pairs[i][0]),
                    nextus=User.objects.get(username=user_pairs[i][1])
                    )
            else:
                usinroute = UserInRoute(
                    route=road,
                    prevus=User.objects.get(username=user_pairs[i][0])
                    )
            usinroute.save()
        msg = message_in_route(request, creator, receiver)
        if msg == False:
            return render(request,'mail/create_route.html')
        message = Message.objects.filter(id=msg).first()
        message.in_route = True
        message.save()
        rmj = RouteMessageJournal(
            prev_user=creator,
            next_user=receiver,
            message_id=message,
            route_id=road)
        rmj.save()
        return redirect("messages")


def message_in_route(request, sender, receiver):
        data = request.POST.copy()
        if receiver:
            data.update({"receiver":receiver.id})
        else:
            data.update({"draft":True})
        fileform = FileForm(request.POST, request.FILES)
        form = DocumentForm(data, request.FILES)
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
                if request.POST.get('id_route') != '':
                    message.in_route=True
                message.save()
                return message.id
        else:
            return False
