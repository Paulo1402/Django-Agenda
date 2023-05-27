from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest
from django.db.models import Q
from contact import models


def index(request: HttpRequest):
    # pylint: disable=E1101
    contacts = models.Contact.objects.filter(show=True).order_by("-id")
    context = {"contacts": contacts, "site_title": "Contatos - "}

    return render(request, "contact/index.html", context)


def search(request: HttpRequest):
    search_value = request.GET.get("q", "").strip()

    if not search_value:
        return redirect("contact:index")

    first_name = ""
    last_name = ""

    try:
        first_name, last_name = search_value.split(maxsplit=1)
    except ValueError:
        pass

    # pylint: disable=E1101
    contacts = (
        models.Contact.objects.filter(show=True)
        .filter(
            Q(first_name__icontains=search_value)
            | Q(last_name__icontains=search_value)
            | Q(phone__icontains=search_value)
            | Q(email__icontains=search_value)
            | Q(first_name__icontains=first_name, last_name__icontains=last_name)
        )
        .order_by("-id")
    )

    context = {"contacts": contacts, "site_title": "Contatos - "}

    return render(request, "contact/index.html", context)


def contact(request: HttpRequest, contact_id: int):
    single_contact = get_object_or_404(models.Contact, id=contact_id, show=True)
    context = {
        "contact": single_contact,
        "site_title": f"{single_contact.first_name} {single_contact.last_name} - ",
    }

    return render(request, "contact/contact.html", context)
