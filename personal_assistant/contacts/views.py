from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Contact
from django.contrib.auth.models import User


# Create your views here.
def main(request):
    contacts = Contact.objects.filter(user=request.user).order_by("name")

    items_per_page = 20
    paginator = Paginator(contacts, items_per_page)

    page = request.GET.get("page")

    try:
        contacts_page = paginator.page(page)
    except PageNotAnInteger:
        contacts_page = paginator.page(1)
    except EmptyPage:
        contacts_page = paginator.page(paginator.num_pages)

    page_range = range(1, contacts_page.paginator.num_pages + 1)

    return render(request, "contacts/index.html", context={"page_title": "contacts list", "contacts": contacts_page, "page_range": page_range})
