synnefo_web_apps = [
    'synnefo.cyclades.api',
    'synnefo.cyclades.ui',
    'synnefo.cyclades.db',
    'synnefo.cyclades.logic',
    'synnefo.cyclades.plankton',
    'synnefo.cyclades.vmapi',
    'synnefo.cyclades.helpdesk',
    'synnefo.cyclades.userdata',
    'synnefo.cyclades.quotas',
    'synnefo.cyclades.volume',
]

synnefo_web_middleware = []
synnefo_web_context_processors = \
    ['synnefo.webproject.context_processors.cloudbar']

synnefo_static_files = {
    'synnefo.cyclades.ui': 'ui/static',
    'synnefo.cyclades.helpdesk': 'helpdesk',
}
