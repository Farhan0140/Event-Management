from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from user.forms import Register_Form, sign_in_form

# Create your views here.


def user_registration(request):
    form = Register_Form()

    if request.method == 'POST':
        form = Register_Form(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "User Created Successfully")
            return redirect("user_registration")

    context = {
        "form": form,
    }

    return render(request, "user_authentication/registration_form.html", context)


def sign_up(request):
    form = sign_in_form()

    if request.method == 'POST':
        form = sign_in_form(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect("#")

    context = {
        'form': form,
    }
    return render(request, "user_authentication/login_form.html", context)


def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')
