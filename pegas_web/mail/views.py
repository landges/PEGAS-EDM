from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from .models import *
from .forms import DocumentForm, FileForm
from django.db.models import Q


# Create your views here.
def main(request):
    return render(request, 'mail/messages.html')


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
                messages = Message.objects.filter(receiver=user, spam=False, is_deleted=False)
            elif type_m == 'sent':
                messages = Message.objects.filter(sender=user, spam=False, is_deleted=False)
            elif type_m == 'draft':
                messages = Message.objects.filter(draft=True, spam=False, is_deleted=False)
            elif type_m == 'trash':
                messages = Message.objects.filter((Q(receiver=user) | Q(sender=user)), is_deleted=True)
            elif type_m == 'trash':
                messages = Message.objects.filter((Q(receiver=user) | Q(sender=user)), spam=True)

        return render(request, 'mail/messages.html', context={"messages": messages.order_by("-date"), "type_m": type_m})

    def post(self, request):
        pass


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
