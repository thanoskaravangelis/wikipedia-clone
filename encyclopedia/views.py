from django.shortcuts import render
from django.http import HttpResponse
from django import forms
import markdown2
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,title):
    if title not in util.list_entries():
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": markdown2.markdown(util.get_entry(title))
        })


def searching(request):
    entries = util.list_entries()
    entries_lower = [s.lower() for s in entries]
    entries_dict = dict(zip(entries_lower,entries))
    
    if 'q' in request.GET:
        search_str = request.GET['q']
    else: 
        return render(request, "encyclopedia/results_error.html",{
            "term":""
        })

    if search_str in entries :
        return entry(request,search_str)
    elif search_str in entries_lower :
        return entry(request, entries_dict[search_str])
    else:
        results = [s for s in entries_lower if search_str.lower() in s]
        if results:
            return render(request, "encyclopedia/results.html", {
                "results":[entries_dict[s] for s in results],
                "term":search_str
            })
        else:
            return render(request, "encyclopedia/results_error.html", {
                "term":search_str
            })

def randompage(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": markdown2.markdown(util.get_entry(title))
    })

class EntryForm(forms.Form):
    new_entry_title = forms.CharField(label='Title',widget=forms.TextInput(attrs={'placeholder': 'Enter the new entry\'s title...'}), max_length = 100 )
    new_entry_text = forms.CharField(label='Details',widget=forms.Textarea(attrs={"rows":20,"cols":40,'placeholder': 'Enter the new entry\'s details in Markdown...'}))

def newentry(request):
    form = EntryForm()
    return render(request , "encyclopedia/newpage.html", {
        "form" : form
    })


        
