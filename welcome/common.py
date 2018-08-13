from django.shortcuts import render
from collections import OrderedDict
from .db import db
PAGE_NAMES = OrderedDict([("wedge_selection", "Selection/Registration"), ("assembly", "Quads & Shims"), ("wiring_1", "Wiring - Layer 1")])

def navbar_template(page_name):
    selected = "wedge_selection"
    for name, caption in PAGE_NAMES.items():
        if name == page_name:
            selected = name
    return {'navbar': list(zip(PAGE_NAMES.keys(), PAGE_NAMES.values())), 'selected' : selected}

def header_template(request):
    return {'title': "Wedge Assembly UI", 'main_heading': "Wedge Assembly UI"}

def status_bar_template(request):
    return {'error': 'wedge_id' in request.session}

def get_wedge_assembly_form_set_factory():
    return modelformset_factory(WedgeAssembly, fields=('quad1', 'shim1'))

def wedge_page_render(request, href, page_name, additional_dict={}):
    template_dict = {}
    template_dict.update(additional_dict)
    template_dict.update(navbar_template(href))
    template_dict.update(header_template(request))
    template_dict.update(status_bar_template(request))
    return render(request, 'welcome/{}.html'.format(page_name), template_dict)


