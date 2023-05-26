from django.shortcuts import render
from contact import models


def index(request):
    contacts = models.Contact.objects.filter(show=True).order_by('-id')  # pylint: disable=E1101

    return render(request, "contact/index.html", {'contacts': contacts})
