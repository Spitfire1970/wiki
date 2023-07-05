from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
import markdown2
import re
import random

class Search_Encyclopedia(forms.Form):
    req_page = forms.CharField(label = '',
            widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))
class Add(forms.Form):
    title = forms.CharField(label = '',
            widget=forms.TextInput(attrs={'placeholder': 'Add page title'}))
    text_area = forms.CharField(label = '',
            widget=forms.Textarea(attrs={'placeholder': 'Add markdown content'}))
class Edit(forms.Form):
    text_area = forms.CharField(label = '',
            widget=forms.Textarea(attrs={'placeholder': 'Edit markdown content'}))
def check_if_page(page):
    bit = 0
    page = page.strip()
    for word in util.list_entries():
        if page.lower() == word.lower():
            bit =1
    return bit
def parse_search(searched):
    li = []
    if check_if_page(searched) == 1:
        return 1
    else:
        for word in util.list_entries():
            if re.search(searched, word, re.IGNORECASE) is not None:
                li.append(word)
        return li
def md_to_html(md_name):
    return markdown2.markdown(util.get_entry(md_name))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": Search_Encyclopedia()})
def show_entry(request, name):
    if check_if_page(name) == 1:
        return render(request, "encyclopedia/show_page.html", {"form":Search_Encyclopedia(),"title":name, "html_required": md_to_html(name)})
    else:
        return render(request, "encyclopedia/error_page.html", {"form":Search_Encyclopedia(),"title":name})
def process_search(request):
    if request.method == "POST":
        form = Search_Encyclopedia(request.POST)
        if form.is_valid():
            res = parse_search(form.cleaned_data["req_page"])
            if res == 1:
                return HttpResponseRedirect("wiki/"+form.cleaned_data["req_page"])
            else:
                return render(request, "encyclopedia/search.html", {"form":Search_Encyclopedia(),"titles":res})
        else:
            return render(request, "encyclopedia/index.html", {"entries": util.list_entries(),"form":form})
def add_page(request):
    if request.method == "POST":
        form = Add(request.POST)
        if form.is_valid():
            ti = form.cleaned_data["title"]
            md = form.cleaned_data["text_area"]
            res = check_if_page(ti)
            if res == 1:
                return render(request, "encyclopedia/add_page.html", {"form1":form,"error_message":"The page you're trying to add already exists!", "form":Search_Encyclopedia()})
            else:
                util.save_entry(ti, md)
                return render(request, "encyclopedia/show_page.html", {"form":Search_Encyclopedia(),"title":ti, "html_required": md_to_html(ti)})
        else:
            return render(request, "encyclopedia/add_page.html", {"form1":form, "error_message":"Invalid input entered!", "form":Search_Encyclopedia()})
    return render(request, "encyclopedia/add_page.html", {"form1":Add(), "error_message":"", "form":Search_Encyclopedia()})
def random_page(request):
    title = random.choice(util.list_entries())
    return HttpResponseRedirect("wiki/" + title)
def edit_page(request, title):
    return render(request, "encyclopedia/edit_page.html", {"name":title, "form2":Edit({'text_area':util.get_entry(title)}), "form":Search_Encyclopedia()})
def edited_page(request, name):
    if request.method == "POST":
        form = Edit(request.POST)
        if form.is_valid():
            res = form.cleaned_data["text_area"]
            util.save_entry(name, res)
            return HttpResponseRedirect(reverse("show_entry", args=(name,)))
        else:
            return HttpResponseRedirect(reverse("edit_page", kwargs={"name": name}))
