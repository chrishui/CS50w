from django import forms
from django.shortcuts import redirect
from django.shortcuts import render
from random import randrange
import markdown2

from . import util

class TitleForm(forms.Form):
    title = forms.CharField(label='',
    widget=forms.Textarea(attrs={'placeholder':'Enter title'}))

class ContentForm(forms.Form):
    content = forms.CharField(label='',
    widget=forms.Textarea(attrs={'placeholder':'Enter Content'}))

# Index page
def index(request):
    # Get request for index page
    return render(request, "encyclopedia/index.html", {
        "title": "Encyclopedia",
        "heading": "All Pages",
        "entries": util.list_entries()
    })

# Wiki entry page for wiki/TITLE
def entry(request, title):
    # if client request matches wiki entry
    if title in util.list_entries():
        # Get request for wiki entry page
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": markdown2.markdown(util.get_entry(title))
        })
    # If client request does not match with wiki entry
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "Entry is not found!"
        })

# Encyclopedia Search
def search(request):
    entries = util.list_entries()
    # Obtain search query from search bar in layout.html
    searchQuery = request.GET.get("q", None)
    # If search matches an entry
    if searchQuery in entries:
        # Redirect to entry page
        return redirect("entry", title=searchQuery)
    # If search partially matches an entry
    else:
        #Filter results
        results = [i for i in entries if searchQuery.lower() in i.lower()]
        return render(request, "encyclopedia/index.html", {
            "title": "Search Results",
            "heading": "Search Results",
            "entries": results
        })

# New page
def newPage(request):
    if request.method == "POST":
        entries = util.list_entries()
        # Obtain new entry title and content
        titleForm = TitleForm(request.POST)
        contentForm = ContentForm(request.POST)

        # If submitted data is valid
        if titleForm.is_valid() and contentForm.is_valid():
            title = titleForm.cleaned_data["title"]
            content = contentForm.cleaned_data["content"]

            # If entry title already exists
            if title in entries:
                # Redirect to error page
                return render(request, "encyclopedia/error.html", {
                    "message": "Entry title already exists!"
                })
            # If no duplications
            else:
                # Save entry to disk and go to new entry's page
                util.save_entry(title, content)
                return redirect("entry", title=title)

    # Get request for new page
    return render(request, "encyclopedia/newPage.html",{
        "title": "Add new page",
        "header": "Add new page",
        "titleForm": TitleForm(),
        "contentForm": ContentForm(),
        "button": "Submit"
    })

# Edit page
def editPage(request, title):
    if request.method == "POST":
        # Obtain new content entry and redirect to entry's page
        contentForm = ContentForm(request.POST)
        # If submitted data is is valid
        if contentForm.is_valid():
            content = contentForm.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect("entry", title=title)

    # Get request for edit page
    else:
        content = util.get_entry(title)
        return render(request, "encyclopedia/editPage.html",{
            "title": "Edit page",
            "header": title,
            "form": ContentForm(initial={'content':content}),
            "button": "Save"
        })

# Random Page
def randomPage(request):
    entries = util.list_entries()
    # Random entry
    randEntry = randrange(len(entries))
    return entry(request, entries[randEntry])
