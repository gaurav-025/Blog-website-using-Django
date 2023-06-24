from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django import forms

class SignUpForm(UserCreationForm):
    username = forms.CharField(label="Username",max_length=30, widget=forms.TextInput(attrs={'class': "form-control"}))
    email = forms.CharField(label="Email",max_length=200, widget=forms.EmailInput(attrs={'class': "form-control"}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': "form-control"}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': "form-control"}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class LoginForm(forms.Form):
    username = forms.CharField(label="Username",max_length=30, widget=forms.TextInput(attrs={'class': "form-control"}))
    # email = forms.CharField(label="Email",max_length=200, widget=forms.EmailInput(attrs={'class': "form-control"}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': "form-control"}))


# Create your views here.
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.add_message(request,messages.SUCCESS, "You have successfully logged in")
                return redirect('blogs:index')
            else:
                # Return an 'invalid login' error message.
                messages.add_message(request, messages.ERROR, "Authentication details were incorrect")
                return redirect("auth:login")
        return render(request, 'login.html', { "form": form})
    form = LoginForm()
    return render(request, "login.html", { "form": form})

def logout_view(request):
    logout(request)
    return redirect('auth:login')

def register_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
        return render(request, 'register.html', { "form": form})
    form = SignUpForm()
    return render(request, "register.html", { "form": form})