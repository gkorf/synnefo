from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'synnefo.cyclades.helpdesk.views.index', name='helpdesk-index'),
    url(r'^actions/vm-suspend/(?P<vm_id>[0-9]+)$',
        'synnefo.cyclades.helpdesk.views.vm_suspend',
        name='helpdesk-suspend-vm'),
    url(r'^actions/vm-suspend-release/(?P<vm_id>[0-9]+)$',
        'synnefo.cyclades.helpdesk.views.vm_suspend_release',
        name='helpdesk-suspend-vm-release'),
    url(r'^actions/vm-shutdown/(?P<vm_id>[0-9]+)$',
        'synnefo.cyclades.helpdesk.views.vm_shutdown',
        name='helpdesk-vm-shutdown'),
    url(r'^actions/vm-start/(?P<vm_id>[0-9]+)$',
        'synnefo.cyclades.helpdesk.views.vm_start',
        name='helpdesk-vm-start'),
    url(r'^(?P<search_query>.*)$', 'synnefo.cyclades.helpdesk.views.account',
        name='helpdesk-details'),
)
