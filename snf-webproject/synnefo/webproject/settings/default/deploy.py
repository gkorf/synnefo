# Copyright 2013 GRNET S.A. All rights reserved.
#
# Redistribution and use in source and binary forms, with or
# without modification, are permitted provided that the following
# conditions are met:
#
#   1. Redistributions of source code must retain the above
#      copyright notice, this list of conditions and the following
#      disclaimer.
#
#   2. Redistributions in binary form must reproduce the above
#      copyright notice, this list of conditions and the following
#      disclaimer in the documentation and/or other materials
#      provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY GRNET S.A. ``AS IS'' AND ANY EXPRESS
# OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL GRNET S.A OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
# USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
# AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and
# documentation are those of the authors and should not be
# interpreted as representing official policies, either expressed
# or implied, of GRNET S.A.

from synnefo.lib.settings.setup import Default

DEBUG = Default(
    default_value=False,
    description="Enable Global Synnefo debug mode.",
    export=False,
)

TEST = Default(
    default_value=False,
    description="Enable Global Synnefo test mode.",
    export=False,
)

# Deployment settings
##################################

TEMPLATE_DEBUG = False

# Use secure cookie for django sessions cookie, change this if you don't plan
# to deploy applications using https
SESSION_COOKIE_SECURE = True

# You should always change this setting.
# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ly6)mw6a7x%n)-e#zzk4jo6f2=uqu!1o%)2-(7lo+f9yd^k^bg'

# A boolean that specifies whether to use the X-Forwarded-Host header in
# preference to the Host header. This should only be enabled if a proxy which
# sets this header is in use.
USE_X_FORWARDED_HOST = True

# Custom exception filter to 'cleanse' setting variables
DEFAULT_EXCEPTION_REPORTER_FILTER = "synnefo.webproject.exception_filter.SynnefoExceptionReporterFilter"
# Settings / Cookies / Headers that should be 'cleansed'
HIDDEN_SETTINGS = 'SECRET|PASSWORD|PROFANITIES_LIST|SIGNATURE|AMQP_HOSTS|'\
                  'PRIVATE_KEY|DB_CONNECTION|TOKEN'
HIDDEN_COOKIES = ['password', '_pithos2_a', 'token', 'sessionid', 'shibstate',
                  'shibsession', 'CSRF_COOKIE']
HIDDEN_HEADERS = ['HTTP_X_AUTH_TOKEN', 'HTTP_COOKIE']
# Mail size limit for unhandled exception
MAIL_MAX_LEN = 100 * 1024  # (100KB)

#When set to True, if the request URL does not match any of the patterns in the
#URLconf and it doesn't end in a slash, an HTTP redirect is issued to the same
#URL with a slash appended. Note that the redirect may cause any data submitted
#in a POST request to be lost. Due to the REST nature of most of the registered
#Synnefo endpoints we prefer to disable this behaviour by default.
APPEND_SLASH = False
