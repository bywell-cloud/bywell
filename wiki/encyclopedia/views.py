from django.shortcuts import render

from . import util

import markdown

from django import forms

from django.urls import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import random


class Enterform(forms.Form):
    title= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),max_length=100)
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'cols': 40 }))
    

class Search(forms.Form):
    q=forms.CharField(widget=forms.TextInput(),max_length=100)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries() ,
    })

def entry_page(request, title):
    try:
        mkd= markdown.Markdown()
        entry = util.get_entry(title)
        return render(request, "encyclopedia/entry.html" , { 
            "title": mkd.convert(entry) , "title2":title
        })

    except:
        return render(request, "encyclopedia/wrongentry.html")

           
def create(request):
    if request.method == "POST":
        form=Enterform(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"] 
            add= util.save_entry(title, body)
            return HttpResponseRedirect(reverse("index"))
            
        else:
            return render(request, "encyclopedia/create.html" ,{ 
                "form":form
            })

    return render(request, "encyclopedia/create.html" , { 
        "form":Enterform()
    })
    
def search(request):
    mkd= markdown.Markdown()
    qcompare=util.list_entries()  
    searchlist=[]  
    if request.method=="GET":
        q= request.GET.get('q')
        searchingmd = util.get_entry(q)
        if searchingmd is not None:
            return render(request, "encyclopedia/entry.html" , { 
                "title": mkd.convert(searchingmd) , "title2":q
            })
        for searching in qcompare:
            if (str.upper(q) in str.upper(searching)):

                searchlist.append(searching) 

        if (len(searchlist) >0):

            return render(request, "encyclopedia/searchresult.html" , { 
               "title2":q ,
               "result":searchlist
            })

        return render(request, "encyclopedia/wrongentry.html" , {
                "title2":q 
            })

def edit(request , title2):
    

    
    if request.method=="POST":
        form = Enterform(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"] 
            add= util.save_entry(title, body)
            return HttpResponseRedirect(reverse("index"))
            
        else:
            return render(request, "encyclopedia/edit.html" ,{ 
                "form":form
            })
    else:
        entry= util.get_entry(title2)
        editform= Enterform({"title":title2,"body":entry})
        return render(request, "encyclopedia/edit.html" ,{ 
                "editform":editform
            })

        

def radpick(request):
    mkd= markdown.Markdown()
    choosing = util.list_entries()
    choiceRan =random.choice(choosing)
    radchoice = util.get_entry(choiceRan)


    return render(request, "encyclopedia/entry.html" , {
        "title2": choiceRan,
        "title": mkd.convert(radchoice)
    })

