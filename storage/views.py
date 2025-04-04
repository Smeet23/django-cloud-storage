from django.shortcuts import render, redirect
from .forms import FileUploadForm
from .models import File
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import File

from django.contrib import messages  # Import this at the top

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save yet
            user.set_password(form.cleaned_data["password1"])  # Hash password
            user.save()
            messages.success(request, "Signup successful! 🎉 You can now log in.")
            return redirect("login")  # Redirect to login after successful signup
        else:
            messages.error(request, "Signup failed. Please check the errors below. 🚨")
    else:
        form = SignupForm()
    
    return render(request, "storage/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("file_list")
    else:
        form = AuthenticationForm()
    return render(request, "storage/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def file_upload_view(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect("file_list")  # Redirect to file list after upload
    else:
        form = FileUploadForm()
    
    return render(request, "storage/file_upload.html", {"form": form})

@login_required
def file_list_view(request):
    files = File.objects.all()  # Get all uploaded files
    return render(request, "storage/file_list.html", {"files": files})

def home(request):
    return render(request, 'home.html')

@login_required
def file_delete(request, pk):
    file = get_object_or_404(File, pk=pk, user=request.user)
    file.file.delete()  # Delete the file from storage
    file.delete()       # Delete the DB entry
    return redirect('file_list')