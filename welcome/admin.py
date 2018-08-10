from django.contrib import admin

from .models import WedgeAssembly

# Register your models here.


class WedgeAssemblyAdmin(admin.ModelAdmin):
    list_display = ['quad1', 'shim1']

admin.site.register(WedgeAssembly, WedgeAssemblyAdmin)
