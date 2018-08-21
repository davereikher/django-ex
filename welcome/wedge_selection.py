from django.http import HttpResponse
from django import forms
from django.forms import ModelForm

from .common import wedge_page_render
from .models import WedgeRegistrationModel
from .db import db
from . import models

import logging
import StylizedFields
from .confirmation import Confirmation
logger = logging.getLogger(__name__)


class WedgeSelectForm(forms.Form):
#    wedge_id = forms.ChoiceField(label='Available wedges', choices=(('1', '20MNMMES100109'), ('2', '20MNMMES100109')))
    wedge_id = forms.ChoiceField(label='Available wedges', choices=[(wedge.pk, "{} ({}, {}, {})".format(wedge.pk, wedge.wedge_l_s, wedge.wedge_p_c, wedge.user_name)) for wedge in WedgeRegistrationModel.objects.all()])
#    wedge_id = forms.ModelChoiceField(label='Available wedges', queryset=WedgeRegistrationModel.objects.all())
    
class RegisterNewWedgeForm(forms.ModelForm):
    class Meta:
        model = models.WedgeRegistrationModel
        fields='__all__'
#        widgets = \
#                { 'creation_date': forms.DateInput(attrs={'class':''}),
#                  'user_name': StylizedFields.MyCharField()
#                        }
        labels = {'wedge_l_s': 'Wedge L/S', 'wedge_p_c': 'Wegde P/C'}


def wedge_selection(request):
    status_msg = "No active wedge. You must select a wedge to work on."
    all_wedges = WedgeRegistrationModel.objects.all()

    #TODO: add a confirmation dialog before registering a new wedge
    logger.debug(str(all_wedges))

    if "wedge_id" in request.session:
        status_msg = "Currently working on wedge with id {}".format(request.session["wedge_id"] )
    
    registered_wedge_ids = [w.wedge_l_s for w in all_wedges]
    logger.debug(registered_wedge_ids)
    wedge_select_form = WedgeSelectForm()
#    wedge_select_form['wedge_id']
    df = db().cmd("SELECT * from ATLAS_MUON_NSW_MM_LOG.EQUIPMENT where OTHERID like 'QL1%'")
    logger.debug(df)
    return wedge_page_render(request, "wedge_selection", "wedge_selection", \
            {"status_msg": status_msg, \
            "wedge_select_form": wedge_select_form, \
            'wedge_register_form': RegisterNewWedgeForm(), \
            'confirmation_js_details': [("select_existing", "select_existing"), ("register_new", "register_new")]})

def do_select_existing(request, post_data):
    logger.debug("Confirmed selecting existing wedge form {}".format(post_data))
    form = WedgeSelectForm(post_data)
    form.is_valid()
    logger.debug("Setting new wedge as active (wedge id={})".format(form.cleaned_data['wedge_id']))
    request.session['wedge_id'] = form.cleaned_data['wedge_id']
    return wedge_selection(request)

def select_existing(request):
    #logger.debug("VALID!. value is {}".format(forms.wedge_id))
    if request.method == "POST":
        form = WedgeSelectForm(request.POST)
        logger.debug(form)
        if form.is_valid():
            return Confirmation('select_existing', request.session, request.POST).render(request,  "Select new wedge with id {} as the active wedge?".format(form.cleaned_data['wedge_id']),\
                    "wedge_confirmation")
    return HttpResponse(status=204)

def do_register_new(request, post_data):
    logger.debug("Confirmed saving form {}".format(post_data))
    form = RegisterNewWedgeForm(post_data)
    logger.debug("Saving")
    form.save()
    return wedge_selection(request)
    
def wedge_confirmation(request):
    if 'pending_confirmation' not in request.session:
        return HttpResponse(status=204)

    d = request.session['pending_confirmation']
    del request.session['pending_confirmation']
    conf_arg = d['arg']
    expected_conf_id = d['id']

    received_conf_id = request.GET.get('id')
    if received_conf_id != expected_conf_id:
        logger.debug("Expected id is not received id during confirmation. Expected: {}, received: {}".format(expected_conf_id, received_conf_id))
        # TODO: show error to user
        return HttpResponse(status=204)
   
    if expected_conf_id == 'register_new':
        return do_register_new(request, conf_arg)
    elif expected_conf_id == 'select_existing':
        return do_select_existing(request, conf_arg)

       
    #TODO: return error here
    return HttpResponse(status=204) 


def register_new(request):
    if request.method == "POST":
        form = RegisterNewWedgeForm(request.POST)

        if form.is_valid():
            return Confirmation('register_new', request.session, request.POST).render(request,  "This will add a new wedge. Are you sure?", "wedge_confirmation")
    return HttpResponse(status=204)
