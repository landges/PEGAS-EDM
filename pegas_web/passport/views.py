from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.base import View
from .models import *
from .forms import *

# Create your views here.
class Regestration(View):
    def get(self, request):
        form1 = SignUpForm()
        form2 = ProfileForm()
        return render(request, 'passport/regestration.html', context={"form1": form1,"form2":form2})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.refresh_from_db()
            form2 = ProfileForm(request.POST)
            #newly added
            user.profile.phone = request.POST['phone']
            user.profile.patronomic = request.POST['patronomic']
 
            # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
 
            # login user after signing up
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/mail/messages/')
        else:
            return redirect('/passport/welcome/')

def logout_view(request):
    logout(request)
    return redirect('/passport/login/')