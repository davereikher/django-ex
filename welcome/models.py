from django.db import models
from django.forms import ModelForm
from . import wedge_utils as wu

# Create your models here.

class WedgeAssembly(models.Model):
    quad1 = models.CharField(max_length=32, choices=wu.get_list_of_available_quads("L1"))
    shim1 = models.CharField(max_length=32)

# models.DateTimeField(auto_now_add=True)

#class PageViewForm(ModelForm):
#    class Meta:
#        model = PageView
#        fields = ['hostname', 'timestamp']
#

