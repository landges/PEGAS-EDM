from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from .models import *
<<<<<<< Updated upstream
from .forms import DocumentForm, FileForm
=======
from passport.models import *
from .forms import DocumentForm, FileForm, RoadForm
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import os
from docx import Document
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from docxtpl import DocxTemplate
>>>>>>> Stashed changes

# Create your views here.
def main(request):
    return render(request,'mail/massages.html')

class Mail(View):
    def get(self, request):
        type_m=request.GET.get('type', 'inbox')
        print(type_m, 'MAIL')
        user = User.objects.get(username=request.user)
        messages=[]
        if type_m == 'inbox':
            messages = Message.objects.filter(receiver=user)
        elif type_m == 'sent':
            messages = Message.objects.filter(sender=user)
        elif type_m == 'draft':
            messages = Message.objects.filter(draft=True)
<<<<<<< Updated upstream
        return render(request,'mail/messages.html',context={"messages":messages.order_by("-date"),"type_m":type_m})
=======
        elif type_m == 'template':
            templates = Templates.objects.all()
            return render(request,'mail/templates.html', context={"templates":templates,"type_m":type_m, "userisboss":userisboss})
        return render(request,'mail/messages.html',context={"messages":messages.order_by("-date"),"type_m":type_m, "userisboss":userisboss})
>>>>>>> Stashed changes
    
    def post(self,request):
        pass

<<<<<<< Updated upstream
class MessageDetailView(DetailView):
    model = Message
=======
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
>>>>>>> Stashed changes


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
                    message.files.add(file)
                message.save()
            return redirect("messages")
        else:
<<<<<<< Updated upstream
            return render(request,'mail/compose.html',context={"fileform":fileform,"mform":form})
=======
            return False


class CreateDocument(View):
    def post(self,request):
        print(request.POST)
        try:
            file_path = request.POST['file']
            os.system('start ' + 'media/' + file_path)
        except KeyError:
            os.system('start docx/New.docx')
        return JsonResponse({"status": "OK"})


class TemplateView(View):
    def post(self, request):
       pass

    def get(self, request, pk):
        template = Templates.objects.filter(id=pk)
        template= template.first()
        file_name = template.file
        tags = template.tags.all()
        return render(request, 'mail/template_detail.html', context={'template': template,
                                                                     'tags': tags,
                                                                     'file':file_name})




def create_file(request):
    data = request.POST.copy()

    path_file_old = 'docx/' + data['file']

    path_file_new = data['path']
    dic_for_render = {}
    for key in data:
        dic_for_render[key] = data[key]
    print(dic_for_render)
    doc = DocxTemplate(path_file_old)
    doc.render(dic_for_render)
    doc.save(path_file_new)

    # user_list = request.POST.getlist()
    # print(user_list)
    return redirect("compose")
>>>>>>> Stashed changes
