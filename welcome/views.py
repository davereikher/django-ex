import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

from . import database
from .models import PageView
import logging
import ipdb

# Create your views here.

logger = logging.getLogger(__name__)

def assembly(request):
    hostname = request.get_host
    PageView.objects.create(hostname=hostname)

    return render(request, 'welcome/assembly.html')

def wiring(request):
    hostname = request.get_host
    PageView.objects.create(hostname=hostname)

    return render(request, 'welcome/wiring.html')

def home(request):
    return HttpResponse(PageView.objects.count())
