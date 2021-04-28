from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return  render(request, 'sign_up/sign_up.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'sign_up/sign_up.html', {'form': form})
