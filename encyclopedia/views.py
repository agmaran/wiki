from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    if request.method == "POST":
        title = request.POST.get('title')
        content = util.get_entry(title)
        if content == None:
            matches = []
            entries = util.list_entries()
            for entry in entries:
                if title.lower() in entry.lower():
                    matches.append(entry)
            return render(request, "encyclopedia/search.html", {
                "matches": matches
            })
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": util.get_entry(title)
    })

def new(request):
    return render(request, "encyclopedia/new.html")
