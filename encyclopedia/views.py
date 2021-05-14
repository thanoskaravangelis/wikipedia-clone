from django.shortcuts import render, redirect
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
    new_entry_title = forms.CharField(label='Title',widget=forms.TextInput(attrs={'placeholder': 'Enter the new entry\'s title...'}), max_length = 100 , initial='')
    new_entry_text = forms.CharField(label='Details',widget=forms.Textarea(attrs={"rows":20,"cols":40,'placeholder': 'Enter the new entry\'s details in Markdown...'}), initial='')

def newentry(request):
    form = EntryForm()
    return render(request , "encyclopedia/newpage.html", {
        "form" : form
    })

def save_new(request):
    title = request.POST['new_entry_title']
    text = request.POST['new_entry_text']
    entries = util.list_entries()
    if title in entries:
        return render(request, "encyclopedia/error.html")
    else:
        util.save_entry(title,text)
        return redirect(f'/wiki/{title}')

class EditEntryForm(forms.Form):
    new_entry_title = forms.CharField(label='Title',widget=forms.TextInput(attrs={'placeholder': 'Enter the new entry\'s title...'}), max_length = 100 , initial='')
    new_entry_text = forms.CharField(label='Details',widget=forms.Textarea(attrs={"rows":20,"cols":40,'placeholder': 'Enter the new entry\'s details in Markdown...'}), initial='')
    old_title = forms.CharField(label='',widget = forms.HiddenInput(), required = False,initial='')

def editentry(request,title):
    content = util.get_entry(title)
    form = EditEntryForm(initial={'new_entry_title':title,
                              'new_entry_text': content,
                              'old_title':title})
    return render(request, "encyclopedia/editpage.html",{
        'title':title,
        'form':form,
        'old_title':title
    })

def save_edited(request):
    title = request.POST['new_entry_title']
    text = request.POST['new_entry_text']
    old_title = request.POST['old_title']
    if old_title == title :
        util.save_entry(title,text)
        return redirect(f'/wiki/{title}')
    else :
        util.delete_entry(old_title)
        util.save_entry(title,text)
        return redirect(f'/wiki/{title}')




        
