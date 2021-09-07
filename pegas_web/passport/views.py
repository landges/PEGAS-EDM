from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.base import View
from .models import *
from .forms import *

# Create your views here.
class Regestration(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'passport/regestration.html', context={"form": form})

    def post(self, request):
        print(request.POST)
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/passport/login/')
        else:
            return redirect('/passport/accounts/regestration/')

def logout_view(request):
    logout(request)
    return redirect('/passport/login/')