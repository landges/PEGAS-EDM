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
import os
from docx import Document
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from docxtpl import DocxTemplate
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def main(request):
    return render(request,'mail/massages.html')

def pagination(request, objects_list, count_of_page):
    paginator = Paginator(objects_list, count_of_page)
    page_number = request.GET.get('page_number', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = 'page_number={0}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = 'page_number={0}'.format(page.next_page_number())
    else:
        next_url = ''
    return (page, is_paginated, prev_url, next_url)

class Mail(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        if request.user.groups.filter(name="boss").exists():
            userisboss = True
        else:
            userisboss = False
        type_m=request.GET.get('type', 'inbox')
        user = User.objects.get(username=request.user)
        messages=[]
        search_query = request.GET.get('request', '')
        if search_query:
            messages = Message.objects.filter(
                (Q(sender__username__icontains=search_query) |
                Q(receiver__username__icontains=search_query) |
                Q(topic__icontains=search_query) |
                Q(text_message__icontains=search_query))&(Q(sender=user) | Q(receiver=user))).order_by('date')
        else:
            if type_m == 'inbox':
                messages = Message.objects.filter(receiver=user,is_truly_deleted=False, is_deleted=False)
            elif type_m == 'sent':
                messages = Message.objects.filter(sender=user,is_truly_deleted=False, is_deleted=False)
            elif type_m == 'draft':
                messages = Message.objects.filter(draft=True,is_truly_deleted=False, is_deleted=False)
            elif type_m == 'trash':
                messages = Message.objects.filter((Q(receiver=user) | Q(sender=user)), is_truly_deleted=False,
                                                  is_deleted=True)
            elif type_m == 'favourite':
                messages = Message.objects.filter((Q(receiver=user) | Q(sender=user)), is_favourite=True, is_deleted=False,
                                                  is_truly_deleted=False)
            elif type_m == 'template':
                templates = Templates.objects.all()
                return render(request,'mail/templates.html', context={"templates":templates,"type_m":type_m, "userisboss":userisboss})
        (page, is_paginated, prev_url, next_url) = pagination(request, messages, 20)
        return render(request,'mail/messages.html',context={"messages":page.object_list,
                                                            "type_m":type_m, 
                                                            "userisboss":userisboss,
                                                            "search_query": search_query,
                                                            "prev_url": prev_url,
                                                            "next_url": next_url}
                                                            )
    

def change_status(request):
    msg_ids = request.POST.get('msgs[]', [])
    if type(msg_ids) is not list:
        msg_ids=[msg_ids,]
    if request.POST.get('type', None) == 'delete':
        for id in msg_ids:
            msg = Message.objects.get(id=id)
            if msg.is_deleted:
                msg.is_truly_deleted = True
            else:
                msg.is_deleted = True
            msg.save()
        return JsonResponse({"complete": True,
                                }, status=200)
    elif request.POST.get('type', None) == 'tofavourite':
        for id in msg_ids:
            msg = Message.objects.get(id=id)
            msg.is_favourite = True
            msg.save()
        return JsonResponse({"complete": True,
                                }, status=200)
    else:
        return JsonResponse({"complete": False}, status=200)

class MessageDetailView(LoginRequiredMixin, View):
    login_url = "login"
    
    def get(self,request,pk):
        fileform = FileForm()
        message=Message.objects.filter(id=pk)
        mform = DocumentForm(message.values()[0])
        message = message.first()
        current_user=User.objects.get(username=request.user)
        if message.receiver == current_user:
            message.read = True
            message.save()
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
            read_in_route = RouteMessageJournal.objects.filter(route_id=id_route.route_id,prev_user=message.receiver).first()
            return render(request,'mail/message_detail.html',context={'message':message,
                "valid_dict":valid_dict,
                'valid': valid,
                "fileform":fileform,
                "mform":mform,
                "id_route":id_route.route_id.id,
                "last_user_in_route":lastuser,
                "read_in_route":read_in_route!=None})
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


class Compose(LoginRequiredMixin, View):
    login_url = "login"

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

class CreateDocument(LoginRequiredMixin, View):
    login_url = "login"
    def post(self,request):
        try:
            file_path = request.POST['file']
            os.system('start ' + 'media\\' + file_path)
        except KeyError:
            os.system('start docx/New.docx')
        return JsonResponse({"status": "OK"})


class TemplateView(LoginRequiredMixin, View):
    login_url = "login"
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

class Create_Route(LoginRequiredMixin, View):
    redirect_url = "login"

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
    print(request.POST)
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