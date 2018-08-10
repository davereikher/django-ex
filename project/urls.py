from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from welcome.views import assembly, wiring, wedge_selection

urlpatterns = [
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', wedge_selection),
    url(r'^assembly$', assembly),
    url(r'^wiring_[0-9]$', wiring),
    url(r'^wedge_selection$', wedge_selection),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
