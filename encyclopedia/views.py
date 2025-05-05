from django.shortcuts import render
from django.shortcuts import render, redirect

from . import views
from . import util

import markdown2
import random

from django.http import HttpResponseRedirect
from django.urls import reverse



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })
    html_content = markdown2.markdown(content)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })


def search(request):
    query = request.GET.get("q")
    entries = util.list_entries()
    matching_entries = [entry for entry in entries if query.lower() in entry.lower()]

    for entry in entries:
        if entry.lower() == query.lower():
            return redirect("entry", title=entry)
        
    return render(request, "encyclopedia/search.html", {
        "query": query,
        "results": matching_entries
    })

    if util.get_entry(query):
        return HttpResponseRedirect(reverse("entry", args=[query]))

    results = [entry for entry in entries if query.lower() in entry.lower()]
    return render(request, "encyclopedia/search.html", {
        "results": results,
        "query": query
    })

def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        if util.get_entry(title):
            return render(request, "encyclopedia/error.html", {
                "message": "An entry with this title already exists."
            })
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", args=[title]))

    return render(request, "encyclopedia/create.html")

def edit(request, title):
    if request.method == "POST":
        content = request.POST["content"]
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", args=[title]))

    content = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })

def random_page(request):
    entries = util.list_entries()
    random_title = random.choice(entries)
    return HttpResponseRedirect(reverse("entry", args=[random_title]))

