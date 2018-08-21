from django.contrib import admin

from .models import WedgeRegistrationModel

# Register your models here.


class WedgeRegistrationModelAdmin(admin.ModelAdmin):
    list_display = ['wedge_l_s', 'wedge_p_c', 'user_name', 'creation_date']

admin.site.register(WedgeRegistrationModel, WedgeRegistrationModelAdmin)
