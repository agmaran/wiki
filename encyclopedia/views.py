from django.shortcuts import render
from django import forms
from . import util
from random import randrange
import markdown2
from django.http import HttpResponseRedirect
from django.urls import reverse


class NewEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    content = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'size': '20'}))


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
        "content": markdown2.markdown(util.get_entry(title))
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
                return HttpResponseRedirect(reverse('entry', args=[form.cleaned_data["title"]]))
    else:
        form = NewEntryForm()
    return render(request, "encyclopedia/new.html", {
        'form': form
    })


def edit(request, title):
    if request.method == "POST":
        util.save_entry(title, request.POST.get('content'))
        return HttpResponseRedirect(reverse('entry', args=[title]))
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": util.get_entry(title)
    })


def random(request):
    entries = util.list_entries()
    random = entries[randrange(len(entries))]
    return HttpResponseRedirect(reverse('entry', args=[random]))
