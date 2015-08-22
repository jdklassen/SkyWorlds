
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login


REGISTER_TEMPLATE = 'skyusers/register.html'


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, REGISTER_TEMPLATE, {'form': form})
