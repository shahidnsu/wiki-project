from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from markdown2 import Markdown
from django import forms
from . import util
import random

markdowner = Markdown()
class editForm(forms.Form):
     content_body = forms.CharField(widget = forms.Textarea(attrs={
        "placeholder":"Contnet Markdown",
        "label" : ""

    }))

class newEntryForm(forms.Form):
    content_title = forms.CharField(widget= forms.TextInput (attrs={
        "label": "",
        "placeholder": "title here"
    }))

    content_body = forms.CharField(widget = forms.Textarea(attrs={
        "placeholder":"Contnet Markdown",
        "label" : ""

    }))    

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entrypage(request, title):
    content = util.get_entry(title)
    if util.get_entry(title):
        content_html = markdowner.convert(content)
        return render(request, "encyclopedia/entrypage.html", {
             "title" : title,
            "content":content_html
        })
    else:
        return render(request, "encyclopedia/404.html",{
            "title" : "404 Error"
        })    
    
# gets  a list of matching entry from search field


def searchentries(entries,title):
     entries_list =[]
     for entry in entries:
         if  title.lower() in entry.lower():
             entries_list.append(entry)
     return entries_list

def search(request):
    
    title = request.POST['q']
    if request.method == 'POST':

       entry =  searchentries(util.list_entries(), title)
       if util.get_entry(title):
          return HttpResponseRedirect(reverse("encyclopedia:entrypage", args=[title]))
       elif entry:
           return render(request, "encyclopedia/index.html", {
               "entries" : entry
           })
       else:
           return render(request, "encyclopedia/404.html", {
               "title": "404 Error"
           })

        

     
def newentry(request):

    if request.method == "POST":
        form = newEntryForm(request.POST)

        if form.is_valid():

            content_title = form.cleaned_data['content_title']
            content_body = form.cleaned_data['content_body']
           
           
            
            entry =  searchentries(util.list_entries(), content_title)
            
            if content_title not in entry:
                util.save_entry(content_title, content_body)
                return HttpResponseRedirect(reverse("encyclopedia:entrypage", args=[content_title]))
            else:
                return HttpResponse("Content already in the wiki")    
                


    return render(request, "encyclopedia/newentry.html", {
        "form" : newEntryForm()
    }) 




def editpage(request,title):
    if request.method == "GET":
        text = util.get_entry(title)

       
        if text == None:
           return render(request, "encyclopedia/404.html",{
               "title": "not exists"
           })

        
        return render(request, "encyclopedia/editpage.html", {
          "title": title,
          "form": editForm(initial={'content_body': text})
          
        })

    
    elif request.method == "POST":
        form = editForm(request.POST)

        if form.is_valid():
          text = form.cleaned_data['content_body']
          util.save_entry(title, text)
          
          return redirect(reverse('encyclopedia:entrypage', args=[title]))

        else:
          
          return render(request, "encyclopedia/editpage.html", {
            "title": title,
            "form": form
            
          })
    
def random_title(request):

    titles  = util.list_entries()
    title = random.choice(titles)
    return HttpResponseRedirect(reverse("encyclopedia:entrypage", args=[title]))
       
    
        



        
