from django.shortcuts import redirect, render
from . import util
from django import forms
from random import sample
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
  entry = util.get_entry(title)
  if entry:
    return render(request, "encyclopedia/entry.html", {
      "entry": markdown2.markdown(entry),
      "title": title
    })
  else:
    return render(request, "encyclopedia/error.html", {
      "error": "not a valid page"
    })

def search(request):
  entries = []
  for entry in util.list_entries():
    if request.GET['q'] in entry:
      entries.append(entry)
  return render(request, "encyclopedia/search.html", {
    "entries": entries
  })

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    entry_body = forms.CharField(widget=forms.Textarea)

def new(request):
  if request.method == "GET":
    return render(request, "encyclopedia/new.html", {
      "form": NewEntryForm()
    })
  else:
    title = request.POST['title']
    body = request.POST['entry_body']
    if util.get_entry(title):
      return render(request, "encyclopedia/error.html", {
        "error": "already exists"
      })
    else:
      util.save_entry(title, body)
      return redirect("entry", title=title)

def edit(request, title):
  if request.method == "GET":
    return render(request, "encyclopedia/edit.html", {
      "body": util.get_entry(title),
      "title": title
    })
  elif request.method == "POST":
    entry = util.save_entry(title, request.POST['entry_body'])
    return redirect("entry", title=title)

def random(request):
  entry = sample(util.list_entries(), 1)[0]
  print(entry)
  return redirect("entry", title=entry)