from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from markdown2 import Markdown

import random

from . import util


class SearchForm(forms.Form):
    search = forms.CharField(label='', widget=forms.TextInput(attrs={"class": "form-control"}))


class CreateForm(forms.Form):
    title = forms.CharField(label='Title', widget=forms.TextInput())
    content = forms.CharField(label='Content', widget=forms.Textarea())


markdowner = Markdown()


def search(request, ask):
    res = []
    entries = util.list_entries()
    for i in entries:
        if i.lower() == ask.lower():
            res.append(i)
            return render(request, "encyclopedia/search_results.html", {
                "entries": res,
                "form": SearchForm()
            })
    for i in entries:
        if ask.lower() in i.lower():
            res.append(i)
    if len(res) > 0:
        return render(request, "encyclopedia/search_results.html", {
            "entries": res,
            "form": SearchForm()
        })
    else:
        return render(request, "encyclopedia/no_results.html", {
            "form": SearchForm()
        })


def index(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            ask = form.cleaned_data['search']
            return search(request, ask)
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": SearchForm()
    })


def file(request, src):
    text = util.get_entry(src)
    text = markdowner.convert(text)
    return render(request, "encyclopedia/main.html", {
        "src": src,
        "text": text,
        "form": SearchForm()
    })


def randomize(request):
    entries = util.list_entries()
    res = random.choice(entries)
    return file(request, res)


def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title, content)
    return render(request, "encyclopedia/create.html", {
        "create_form": CreateForm(),
        "form": SearchForm()
    })


def edit(request, src):

    content = util.get_entry(src)

    class EditForm(forms.Form):
        contents = util.get_entry(src)
        title = forms.CharField(label='Title', widget=forms.TextInput(attrs={"value": src}))
        content = forms.CharField(label='Content', widget=forms.Textarea(attrs={"value": contents}))
    form = CreateForm(request.POST)
    if form.is_valid():
        content = form.cleaned_data['content']
        filename = f"entries/{src}.md"
        default_storage.delete(filename)
        default_storage.save(filename, ContentFile(content))

    return render(request, "encyclopedia/edit.html", {
        "edit_form": EditForm(),
        "form": SearchForm()
    })