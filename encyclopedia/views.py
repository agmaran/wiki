from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": util.get_entry(title)
    })


def search(request):
    title = request.POST.get("title")
    if util.get_entry(title) == None:
        matches = []
        entries = util.list_entries()
        for entry in entries:
            if title in entry:
                matches.append(entry)
        return render(request, "encyclopedia/search.html", {
            "matches": matches
        })
    return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": util.get_entry(title)
    })
    
