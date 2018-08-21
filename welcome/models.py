from django.db import models
from django.forms import ModelForm
from . import wedge_utils as wu

# Create your models here.

class WedgeRegistrationModel(models.Model):
    wedge_l_s = models.CharField(choices=(("L", "Large"), ("S", "Small")), max_length=1)
    wedge_p_c = models.CharField(choices=(("P", "Pivot"), ("C", "Confirm")), max_length=1)
    user_name = models.CharField(max_length=32)
    creation_date = models.DateField()


# models.DateTimeField(auto_now_add=True)

#class PageViewForm(ModelForm):
#    class Meta:
#        model = PageView
#        fields = ['hostname', 'timestamp']
#

