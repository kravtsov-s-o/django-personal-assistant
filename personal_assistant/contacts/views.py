from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from .models import Contact
from .forms import AddContact


# Create your views here.
@login_required(login_url='/signin/')
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

    return render(request, "contacts/index.html", context={"page_title": "Contacts List", "contacts": contacts_page, "page_range": page_range})


@login_required(login_url='/signin/')
def add_contact(request):

    if request.method == 'POST':
        form = AddContact(request.POST)

        if form.is_valid():
            new_contact = form.save(commit=False)
            new_contact.user = request.user
            new_contact.save()

            return redirect(to="contacts:main")
        else:
            return render(request, "contacts/add-contact.html", {"page_title": "New contact", "form": form})

    return render(
        request,
        "contacts/add-contact.html",
        context={"page_title": "New contact", "form": AddContact},
    )


@login_required(login_url='/signin/')
def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    contact.delete()
    return redirect("contacts:main")


@login_required(login_url='/signin/')
def edit_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    if request.method == "POST":
        form = AddContact(request.POST, instance=contact)

        if form.is_valid():
            form.save()

            return redirect(to="contacts:main")
        else:
            return render(
                request,
                "contacts/add-contact.html",
                {"page_title": "Edit contact", "contact": contact, "form": form},
            )

    form = AddContact(instance=contact)
    return render(
        request, "contacts/add-contact.html", {"page_title": "Edit contact", "contact": contact, "form": form}
    )
