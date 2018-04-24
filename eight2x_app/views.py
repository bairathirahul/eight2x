from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('login')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
        for field in form.fields:
            print(field)
            form.fields[field].widget.attrs['class'] = 'form-control'
    
    return render(request, 'eight2x_app/register.html', {'form': form})


def dashboard(request):
    return render(request, 'eight2x_app/dashboard.html')


def detail(request):
    pass


def issues(request):
    pass


def reply(request):
    pass

# Create your views here.
