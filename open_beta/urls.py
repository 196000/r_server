from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'open_beta.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^server/', include('server.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
	#url(r'^accounts/', include('registration.backends.simple.urls')),
)

urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )