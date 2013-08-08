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

from synnefo.settings.setup import Mandatory, Default


ADMINS = Default(
    default_value=[],
    example_value=[
        ("John Smith", "john@example.synnefo.org"),
        ("Mary Smith", "mary@example.synnefo.org"),
    ],
    description="List of people who receive application notifications, such as "
        "code error tracebacks. It is recommended to have at least one entry "
        "in this list.",
    category="snf-common-admins",
    export=True,
)

HELPDESK = Default(
    default_value=[],
    example_value=[
        ("John Smith", "john@example.synnefo.org"),
        ("Mary Smith", "mary@example.synnefo.org"),
    ],
    description="List of people who receive user feedback notifications. ",
    category="snf-common-admins",
    export=True,
)

MANAGERS = Default(
    default_value=[],
    example_value=[
        ("John Smith", "john@example.synnefo.org"),
        ("Mary Smith", "mary@example.synnefo.org"),
    ],
    description="List of people who receive email on some application events. "
        "(e.g.: account creation/activation).",
    category="snf-common-admins",
    export=True,
)

#
# Email server configuration
#

EMAIL_HOST = Default(
    default_value="127.0.0.1",
    description="IP or domain of the smtp server that will be used by Synnefo.",
    category="snf-common-admins",
    export=True,
)

EMAIL_PORT = Default(
    default_value=25,
    description="The smtp server's port to connect to.",
    category="snf-common-admins",
    export=True,
)

EMAIL_HOST_USER = Default(
    default_value="",
    example_value="JohnSmith",
    description="",
    category="snf-common-admins",
    export=True,
)

# Synnefo logging directory
############################

# Directory where log files are saved
# Currently only snf-manage uses this to save
# the output of the commands being executed.
LOG_DIR = "/var/log/synnefo/"

EMAIL_HOST_PASSWORD = Default(
    default_value="",
    description="The user's password.",
    category="snf-common-admins",
    export=True,
)

EMAIL_SUBJECT_PREFIX = Default(
    default_value="[synnefo] ",
    description="Add this prefix to all email subjects sent by the service.",
    category="snf-common-admins",
    export=True,
)

DEFAULT_FROM_EMAIL = Default(
    default_value="synnefo <no-reply@synnefo.org>",
    example_value="service_name <no-reply@service_name.com>",
    description="Address to use for outgoing emails.",
    category="snf-common-admins",
    export=True,
)

CONTACT_EMAIL = Default(
    default_value="support@example.synnefo.org",
    example_value="support@service_name.com",
    description="Email where users can contact for support. Will appear in "
        "emails and UI.",
    category="snf-common-admins",
    export=True,
)

SERVER_EMAIL = Default(
    default_value="Synnefo cloud <cloud@example.synnefo.org>",
    example_value="service_name <service_name@service_name.com>",
    description="Email address the emails sent by the service will come from.",
    category="snf-common-admins",
    export=True,
)

DEFAULT_CHARSET = Default(
    default_value="utf-8",
    description="The default charset.",
    export=False,
)
