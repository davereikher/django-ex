from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from welcome.wedge_assembly import assembly
from welcome.wedge_selection import wedge_selection, select_existing, register_new, wedge_confirmation
from welcome.wedge_wiring import wiring

urlpatterns = [
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', wedge_selection),
    url(r'^assembly$', assembly),

    url(r'^select_existing$', select_existing), 
    url(r'^register_new$', register_new),
    url(r'^wedge_confirmation$', wedge_confirmation),
    
    url(r'^wiring_[0-9]$', wiring), #TODO: limit to 0-maximum (not 0-9)
    url(r'^wedge_selection$', wedge_selection),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
