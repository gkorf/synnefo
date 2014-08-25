# -*- coding: utf-8 -*-
#
# Logging configuration
##################################
from synnefo.lib.settings.setup import Default
from synnefo.util.entry_points import extend_list_from_entry_point, \
        extend_dict_from_entry_point


_FORMATTERS = {
    'simple': {
        'format': '%(asctime)s [%(levelname)s] %(message)s'
    },
    'verbose': {
        'format': '%(asctime)s [%(process)d] %(name)s %(module)s [%(levelname)s] %(message)s'
    },
    'django': {
        'format': '[%(asctime)s] %(levelname)s %(message)s',
        'datefmt': '%d/%b/%Y %H:%M:%S'
    },
}

_LOGGERS = {
    '': {
        'handlers': ['console'],
        'level': 'INFO'
    },
    'django.request': {
        'handlers': ['mail_admins'],
        'level': 'ERROR',
        'propagate': True,
    },
    'synnefo': {
        'handlers': ['console'],
        'level': 'INFO',
        'propagate': 0
    },
}

LOGGING_SETUP = Default(
    default_value={
        'version': 1,
        'disable_existing_loggers': False,

        'formatters': _FORMATTERS,
        'handlers': {
            'null': {
                'class': 'logging.NullHandler',
            },
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
            'syslog': {
                'class': 'logging.handlers.SysLogHandler',
                'address': '/dev/log',
                # 'address': ('localhost', 514),
                'facility': 'daemon',
                'formatter': 'verbose',
                'level': 'INFO',
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
                'include_html': False,
            }
        },

        'loggers': extend_dict_from_entry_point(
            _LOGGERS, 'synnefo', 'loggers'),
    },
    description="Logging setup",
    category="snf-webproject-logging",
    export=False,
)

#LOGGING_SETUP['loggers']['synnefo.cyclades.admin'] = {'level': 'INFO', 'propagate': 1}
#LOGGING_SETUP['loggers']['synnefo.cyclades.api'] = {'level': 'INFO', 'propagate': 1}
#LOGGING_SETUP['loggers']['synnefo.cyclades.db'] = {'level': 'INFO', 'propagate': 1}
#LOGGING_SETUP['loggers']['synnefo.cyclades.logic'] = {'level': 'INFO', 'propagate': 1}

# To set logging level for plankton to DEBUG just uncomment the follow line:
# LOGGING_SETUP['loggers']['synnefo.cyclades.plankton'] = {'level': 'INFO', 'propagate': 1}

SNF_MANAGE_LOGGING_SETUP = Default(
    default_value={
        'version': 1,
        'disable_existing_loggers': False,

        'formatters': _FORMATTERS,

        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
        },

        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'WARNING'
            },
        }
    },
    description="snf-manage logging setup",
    category="snf-webproject-logging",
    export=False,
)
