from django.conf.urls import patterns, url
# from django.views.generic import TemplateView


urlpatterns = patterns('',
    url(r'^analytics/$', 'analytics.views.portal', name='portal'),
    url(r'^detail_view/(\d+)/$', 'analytics.views.detail_view', name='detail_view'),
    url(r'^error/$', 'analytics.views.error', name='error'),
)
