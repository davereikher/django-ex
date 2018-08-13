from .common import wedge_page_render
from .models import WedgeAssembly 
from .db import db
from django import forms

import logging

logger = logging.getLogger(__name__)

class WedgeSelectForm(forms.Form):
    wedge_id = forms.ChoiceField(label='avail_wedges', choices=(("blah", "BLAH"), ("moo","MOO")))
    
def wedge_selection(request):
    status_msg = "No active wedge. You must select a wedge to work on."
    if "wedge_id" in request.session:
        status_msg = "Currently working on wedge with id {}".format(request.session["wedge_id"] )
   
    df = db().cmd("SELECT * from ATLAS_MUON_NSW_MM_LOG.EQUIPMENT where OTHERID like 'QL1%'")
    logger.debug(df)
    return wedge_page_render(request, "wedge_selection", "wedge_selection", {"status_msg": status_msg, "wedge_select_form": WedgeSelectForm()})

def select_existing(request):
    #logger.debug("VALID!. value is {}".format(forms.wedge_id))
    logger.debug("HERE!")
    if request.method == "POST":
        form = WedgeSelectForm(request.POST)
        logger.debug(form)
        if form.is_valid():
            request.session['wedge_id'] = form.cleaned_data['wedge_id']
    return wedge_selection(request)


