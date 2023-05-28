from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpRequest
from django.db.models import Q

from contact.models import Contact


def index(request: HttpRequest):
    # pylint: disable=E1101
    contacts = Contact.objects.filter(show=True).order_by("-id")

    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "site_title": "Contatos - ",
    }

    return render(request, "contact/index.html", context)


def search(request: HttpRequest):
    search_value = request.GET.get("q", "").strip()

    if not search_value:
        return redirect("contact:index")

    filters = (
        Q(first_name__icontains=search_value)
        | Q(last_name__icontains=search_value)
        | Q(phone__icontains=search_value)
        | Q(email__icontains=search_value)
    )

    try:
        first_name, last_name = search_value.split(maxsplit=1)
        filters |= Q(
            Q(first_name__icontains=first_name) & Q(last_name__icontains=last_name)
        )
    except ValueError:
        pass

    # pylint: disable=E1101
    contacts = Contact.objects.filter(show=True).filter(filters).order_by("-id")

    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "site_title": "Contatos - ",
        "search_value": search_value,
    }

    return render(request, "contact/index.html", context)


def contact(request: HttpRequest, contact_id: int):
    single_contact = get_object_or_404(Contact, id=contact_id, show=True)
    context = {
        "contact": single_contact,
        "site_title": f"{single_contact.first_name} {single_contact.last_name} - ",
    }

    return render(request, "contact/contact.html", context)
