from django.shortcuts import render
import urllib3
import time

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect , HttpResponse

from .forms import *

from lxml import html
import csv, os, json
import requests
from django.utils import timezone
#from selenium import webdriver
import bs4 as bs
import urllib3
from django.urls import reverse

# Create your views here.
def home(request):
    return render(request,'dimension/index.html')
def dimension(request):
    return render(request,'dimension/index.html')
def hackoverflow(request):
    return render(request,'dimension/hackoverflow.html')

#####################################################################################

############################# 2019 Dimension Work  #########################################

def confrence(request):

    if request.method == "POST":
        form = ConfrenceSignupForm(request.POST)
        if form.is_valid():
            confrence = form.save(commit=False)
            confrence.save()
            return HttpResponse('Form submitted Successfully')

        else:
        	form = ConfrenceSignupForm()
        	errors = "form is not filled correctly"

        return render(request, 'dim2019/confrence_form.html', {'form': form ,'errors':errors})

    else:
    	form = ConfrenceSignupForm()
    	return render(request, 'dim2019/confrence_form.html', {'form': form })

def anime(request):
	return render(request, 'dim2019/layouts/try.html')