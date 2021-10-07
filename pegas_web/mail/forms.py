from django.forms import fields, widgets
from .models import File, Message
from django import forms


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Message
        # exclude=('sender',)
        fields = ('receiver', 'topic', 'text_message','draft', 'files')
        widgets = {
            "receiver": forms.TextInput(attrs={"name":"receiver","class":"b-form-input__input"}),
            "topic": forms.TextInput(attrs={"name":"subj","class":"b-form-input__input"}),
            "text_message": forms.Textarea(attrs={"class":"b-form-textarea","name":"send","id":"compose-send", "cols":30, "rows":10,"aria-label":"Тело письма"})
        }

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('file',)
        widgets = {
            "file":forms.ClearableFileInput(attrs={'multiple': True,"class":"b-compose__file"})
        }

# class RouteForm(forms.ModelForm):
#     class Meta:
#         model = Route
#         fields = ('sender', 'receiver')
        