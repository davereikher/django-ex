import os
import pandas as pd
from .db import db
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.forms import modelformset_factory

from . import database
from .models import WedgeAssembly 
import logging
import ipdb
from collections import OrderedDict

# Create your views here.

logger = logging.getLogger(__name__)

PAGE_NAMES = OrderedDict([("wedge_selection", "Selection/Registration"), ("assembly", "Quads & Shims"), ("wiring_1", "Wiring - Layer 1")])

#class WedgeAssemblyForm(ModelForm):
#    quad1 = 
#    class Meta:
#        model = WedgeAssembly
#        fields = ['quad1', 'shim1']
#        widgets = 
#

def navbar_template(page_name):
    selected = "wedge_selection"
    for name, caption in PAGE_NAMES.items():
        if name == page_name:
            selected = name
    return {'navbar': list(zip(PAGE_NAMES.keys(), PAGE_NAMES.values())), 'selected' : selected}

def header_template(request):
    return {'title': "Wedge Assembly UI", 'main_heading': "Wedge Assembly UI"}

def status_bar_template(request):
    return {'error': 'wedge_id' not in request.session}

def get_wedge_assembly_form_set_factory():
    return modelformset_factory(WedgeAssembly, fields=('quad1', 'shim1'))

def wedge_page_render(request, href, page_name, additional_dict={}):
    template_dict = {}
    template_dict.update(additional_dict)
    template_dict.update(navbar_template(href))
    template_dict.update(header_template(request))
    return render(request, 'welcome/{}.html'.format(page_name), template_dict)

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

def assembly(request):
    if 'wedge_id' not in request.session:
        return wedge_selection(request)

    WedgeAssemblyFormSet = get_wedge_assembly_form_set_factory()
    formset = WedgeAssemblyFormSet()

    return wedge_page_render(request, "assembly", "assembly", {'formset': formset})

def wedge_selection(request):
    status_msg = "No active wedge. You must select a wedge to work on."
    if "wedge_id" in request.session:
        status_msg = "Currently active wedge: {}".format(request.session["wedge_id"] )
   
    df = db().cmd("SELECT * from ATLAS_MUON_NSW_MM_LOG.EQUIPMENT where OTHERID like 'QL1%'")
    logger.debug(df)
    return wedge_page_render(request, "wedge_selection", "wedge_selection", {"status_msg": status_msg})

#     return render(request, 'welcome/assembly.html')

def wiring(request):
    return wedge_page_render(request, 'wiring_1', 'wiring')

def home(request):
    return HttpResponse(PageView.objects.count())
