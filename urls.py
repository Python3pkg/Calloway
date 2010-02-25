from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps import FlatPageSitemap

admin.autodiscover()

from news_sitemaps import NewsSitemap
from stories.models import Story

handler500 = 'django_ext.views.custom_server_error'

class StorySitemap(NewsSitemap):
    limit = 5000
    def items(self):
        return Story.published.all()
        
    def lastmod(self, obj):
        return obj.publish_date
    
sitemaps = {
    'flatpages': FlatPageSitemap,
    'stories': StorySitemap    
}

urlpatterns = patterns('',
    (r'^cache/', include('django_memcached.urls')),
    (r'^admin/log/', include('logjam.urls')),
    (r'^admin/varnish/', include('varnishapp.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^api/', include('api.urls')),
    (r'^syn/', include('synagg.urls')),
    (r'^massmedia/', include('massmedia.urls')),
    (r'^sitemaps/', include('news_sitemaps.urls')),
    (r'^news/', include('stories.urls')),
    (r'^frontendadmin/', include('frontendadmin.urls')),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.index', {'sitemaps': sitemaps}),
    (r'^sitemap-stories\.xml', 'news_sitemaps.views.news_sitemap', {'sitemaps': {'stories': sitemaps['stories']}}),    
    (r'^sitemap-(?P<section>.+)\.xml', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^robots.txt', 'robots.views.rules_list', name='robots_rule_list'),
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template':'homepage.html'}),    
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'^media/(?P<path>.*)$', 'serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
