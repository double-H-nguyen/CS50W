from nis import match
from queue import Empty
from django.http import HttpResponseRedirect
from django.shortcuts import render
from . import util


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
        "entry": entry
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