from django.http import HttpRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from contact.forms import ContactForm
from contact.models import Contact


def create(request: HttpRequest):
    form_action = reverse("contact:create")
    # form_action = request.get_full_path()

    if request.method == "POST":
        form = ContactForm(request.POST)
        context = {
            "form": form,
            "form_action": form_action,
        }

        if form.is_valid():
            contact = form.save()
            return redirect("contact:update", contact_id=contact.id)

        return render(request, "contact/create.html", context)

    context = {
        "form": ContactForm(),
        "form_action": form_action,
    }

    return render(request, "contact/create.html", context)


def update(request: HttpRequest, contact_id: int):
    contact = get_object_or_404(Contact, id=contact_id, show=True)
    form_action = reverse("contact:update", args=(contact_id,))
    # form_action = request.get_full_path()

    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        context = {
            "form": form,
            "form_action": form_action,
        }

        if form.is_valid():
            contact = form.save()
            return redirect("contact:update", contact_id=contact.id)

        return render(request, "contact/create.html", context)

    context = {"form": ContactForm(instance=contact), "form_action": form_action}

    return render(request, "contact/create.html", context)


def delete(request: HttpRequest, contact_id: int):
    contact = get_object_or_404(Contact, id=contact_id, show=True)
    confirmation = request.POST.get("confirmation", "no")

    context = {
        "contact": contact,
        "confirmation": confirmation,
    }

    if confirmation == "yes":
        contact.delete()
        return redirect("contact:index")

    return render(request, "contact/contact.html", context)
