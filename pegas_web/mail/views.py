from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from .models import *
from .forms import DocumentForm, FileForm
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator


# Create your views here.
def main(request):
    return render(request, 'mail/messages.html')


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


class Mail(View):
    def get(self, request):
        type_m = request.GET.get('type', 'inbox')
        user = User.objects.get(username=request.user)
        messages = []
        search_query = request.GET.get('request', '')
        if search_query:
            messages = Message.objects.filter(
                Q(sender__username__icontains=search_query) |
                Q(receiver__username__icontains=search_query) |
                Q(topic__icontains=search_query) |
                Q(text_message__icontains=search_query)).order_by('date')
        else:
            if type_m == 'inbox':
                messages = Message.objects.filter(receiver=user, is_truly_deleted=False, is_deleted=False)
            elif type_m == 'sent':
                messages = Message.objects.filter(sender=user, is_truly_deleted=False, is_deleted=False)
            elif type_m == 'draft':
                messages = Message.objects.filter(draft=True, is_truly_deleted=False, is_deleted=False)
            elif type_m == 'trash':
                messages = Message.objects.filter((Q(receiver=user) | Q(sender=user)), is_truly_deleted=False,
                                                  is_deleted=True)
            elif type_m == 'favourite':
                messages = Message.objects.filter((Q(receiver=user) | Q(sender=user)), favourite=True, is_deleted=False,
                                                  is_truly_deleted=False)
        (page, is_paginated, prev_url, next_url) = pagination(request, messages, 20)
        return render(request, 'mail/messages.html', context={"msgd_disp": page.object_list, "type_m": type_m,
                                                              "search_query": search_query,
                                                              "prev_url": prev_url,
                                                              "next_url": next_url})

    def post(self, request):
        msg_ids = request.POST.get('msgs[]', [])
        if type(msg_ids) != list:
            msg_ids = [msg_ids]
        if request.POST.get('type', None) == 'delete':
            for id in msg_ids:
                print(id)
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
            return JsonResponse({"complete": False,
                                 "msgs": []}, status=200)


class MessageDetailView(DetailView):
    model = Message


class Compose(View):
    def get(self, request):
        fileform = FileForm()
        mform = DocumentForm()
        return render(request, 'mail/compose.html', context={"fileform": fileform, "mform": mform})

    def post(self, request):
        data = request.POST.copy()
        fileform = FileForm(request.POST, request.FILES)
        receiver = User.objects.filter(username=request.POST['receiver']).first()
        if receiver:
            data.update({"receiver": receiver.id})
        else:
            data.update({"draft": True})
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
            return render(request, 'mail/compose.html', context={"fileform": fileform, "mform": form})
