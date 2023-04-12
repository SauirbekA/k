from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticated_user
from main.forms import *


from .forms import *

# @unauthenticated_user
def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = form.cleaned_data['group']        
            group.user_set.add(user)
            user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, user)
            return redirect('mainpage')
           
    context = {'form': form, }
    return render(request, 'Register/register.html', context)


login = unauthenticated_user(login)
