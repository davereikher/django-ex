from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from welcome.views import assembly, wiring, home

urlpatterns = [
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', home),
    url(r'^assembly$', assembly),
    url(r'^wiring$', wiring),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
