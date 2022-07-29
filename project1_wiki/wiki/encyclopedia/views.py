from nis import match
from queue import Empty
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from . import util
from . import forms
from random import randint
from markdown2 import markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, title):
    entry = util.get_entry(title)
    if entry is None:
        return render(request, "encyclopedia/error.html", {
            "error_title": "Page Not Found",
            "error_message": f"Sorry, \"{title}\" page does not exist."
        })
    
    return render(request, "encyclopedia/wiki.html", {
        "title": title.capitalize(),
        "entry": markdown(entry)
    })


def search(request):
    if request.method == "POST":
        search = request.POST['q']
        entry = util.get_entry(search)
        if entry is None:
            # show list of available pages that contains the substring
            matched_entries = []
            entries = util.list_entries()
            for entry in entries:
                if search.lower() in entry.lower():
                    matched_entries.append(entry)
            if len(matched_entries) != 0:
                return render(request, "encyclopedia/search_results.html", {
                    "entries": matched_entries
                })
            else: # show no pages found
                return render(request, "encyclopedia/error.html", {
                    "error_title": "No Pages Found Based on Search",
                    "error_message": f"Sorry, no pages were found that matched with \"{search}\"."
                })
        else: # if page is found, redirect to page
            return HttpResponseRedirect(f'/wiki/{search}')


def create(request):
    if request.method == "POST":
        form = forms.create_page_form(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            # if page doesn't exist add to disk and redirect to page, else show error page
            if util.get_entry(title) is None:
                util.save_entry(title, content)
                return HttpResponseRedirect(f'/wiki/{title}')
            else:
                # return original form values with error message
                messages.error(request, f"\"{title.capitalize()}\" page already exist. Use a different title.")
                return render(request, "encyclopedia/create.html", {
                    "form": form   
                })
    else:
        form = forms.create_page_form()
        return render(request, "encyclopedia/create.html", {
            "form": form   
        })


def edit(request, title):
    if request.method == "POST":
        form = forms.edit_page_form(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(f'/wiki/{title}')
        else: # invalid form
            messages.error(request, "Unable to save edit. Please verify your inputs.")
            return render(request, "encyclopedia/edit.html", {
                "title": title.capitalize(),
                "form": form
            })
    else:
        entry = util.get_entry(title)
        if entry is not None: # page exist
            form = forms.edit_page_form(initial={'content': entry})
            return render(request, "encyclopedia/edit.html", {
                "title": title.capitalize(),
                "form": form
            })
        else: # page does not exist
            return render(request, "encyclopedia/error.html", {
                "error_title": "Page does not exist",
                "error_message": f"\"{title.capitalize()}\" page does not exist, so it cannot be edited."
            })


def random(request):
    entries = util.list_entries()
    if entries is not None: # entries exist
        random_title = entries[randint(0, len(entries) - 1)]
        return HttpResponseRedirect(f'wiki/{random_title}')
    else: # no entries
        return render(request, "encyclopedia/error.html", {
                "error_title": "No entries",
                "error_message": "There are no entries, so a random page cannot be selected."
            })