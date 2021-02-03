from django.shortcuts import render
from django import forms
from . import util


class NewEntryForm(forms.Form):
    title = forms.CharField(label='Title for the page')
    content = forms.CharField(
        label='Markdown content for the page', widget=forms.Textarea)


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
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            entries = util.list_entries()
            entries = [entry.lower() for entry in entries]
            if form.cleaned_data["title"].lower() in entries:
                return render(request, "encyclopedia/new.html", {
                    'form': form,
                    'message': "Error! An encyclopedia entry already exists with the provided title."
                })
            else:
                util.save_entry(
                    form.cleaned_data["title"], form.cleaned_data["content"])
                return render(request, "encyclopedia/entry.html", {
                    "title": form.cleaned_data["title"],
                    "content": util.get_entry(form.cleaned_data["title"])
                })
    else:
        form = NewEntryForm()
    return render(request, "encyclopedia/new.html", {
        'form': form
    })


def edit(request, title):
    if request.method == "POST":
        util.save_entry(title, request.POST.get('content'))
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": util.get_entry(title)
        })
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": util.get_entry(title)
    })
