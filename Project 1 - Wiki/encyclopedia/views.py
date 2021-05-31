from django.shortcuts import render
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
  entry = util.get_entry(title)
  if entry:
    return render(request, "encyclopedia/entry.html", {
      "entry": entry
    })
  else:
    return render(request, "encyclopedia/error.html")

def search(request):
  entries = []
  for entry in util.list_entries():
    if request.GET['q'] in entry:
      entries.append(entry)
  return render(request, "encyclopedia/search.html", {
    "entries": entries
  })