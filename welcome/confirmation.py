from django.shortcuts import render
from django.core import serializers
import marshal 

class Confirmation(object):
    def __init__(self, conf_id, session, obj):
        session['pending_confirmation'] = {'arg': obj, 'id': conf_id}
        self._id = conf_id

    def render(self, request, message, request_url, yes_caption="yes", no_caption="no"):
        template_dict = {'confirm_query_message': message, 'confirm_yes_caption': yes_caption, 'confirm_no_caption': no_caption, 'confirm_request_url': request_url, 'confirm_request_id': self._id}
        return render(request, 'welcome/confirmation.html', template_dict)
