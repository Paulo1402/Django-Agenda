from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required

from contact.forms import RegisterForm, RegisterUpdateForm


def register(request: HttpRequest):
    form = RegisterForm()
    form_action = request.get_full_path()

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Usuário registrado")

            return redirect("contact:login")

    context = {
        "form": form,
        "form_action": form_action,
    }

    return render(request, "contact/register.html", context)


def login(request: HttpRequest):
    form = AuthenticationForm(request)
    form_action = request.get_full_path()

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(request, "Logado com sucesso!")

            return redirect("contact:index")

        messages.error(request, "Login inválido!")

    context = {
        "form": form,
        "form_action": form_action,
    }

    return render(request, "contact/login.html", context)


@login_required(login_url="contact:login")
def logout(request: HttpRequest):
    auth.logout(request)
    return redirect("contact:login")


@login_required(login_url="contact:login")
def user_update(request: HttpRequest):
    form = RegisterUpdateForm(instance=request.user)
    form_action = request.get_full_path()

    if request.method == "POST":
        form = RegisterUpdateForm(instance=request.user, data=request.POST)

        if form.is_valid():
            form.save()
            return redirect("contact:user_update")

    context = {
        "form": form,
        "form_action": form_action,
    }

    return render(request, "contact/user_update.html", context)
