import os
import pandas as pd
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.forms import modelformset_factory

from . import database
import logging
import ipdb
from collections import OrderedDict

# Create your views here.

logger = logging.getLogger(__name__)

#class WedgeAssemblyForm(ModelForm):
#    quad1 = 
#    class Meta:
#        model = WedgeAssembly
#        fields = ['quad1', 'shim1']
#        widgets = 
#

def save_assembly(request):
    WedgeAssemblyFormSet = get_wedge_assembly_form_set_factory()
    if request.method == 'POST':
        formset = WedgeAssemblyFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            # do something.

def select_wedge(request):
    pass

def new_wedge(request):
    pass

def home(request):
    return HttpResponse(PageView.objects.count())
