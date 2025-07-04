from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.

from user.forms import Register_Form

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

    return render(request, "user_authentication/registration.html", context)