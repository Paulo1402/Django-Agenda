from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpRequest

from contact.forms import RegisterForm


def register(request: HttpRequest):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário registrado')
            return redirect('contact:index')

    return render(
        request,
        "contact/register.html",
        {
            "form": form,
        },
    )
