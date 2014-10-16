# Copyright (C) 2010-2014 GRNET S.A.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from synnefo.lib.settings.setup import Default


ADMINS = Default(
    default_value=[],
    example_value=[
        ("John Smith", "john@example.synnefo.org"),
        ("Mary Smith", "mary@example.synnefo.org"),
    ],
    description=(
        "List of people who receive application notifications, such as "
        "code error tracebacks. It is recommended to have at least one entry "
        "in this list."),
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
    description=(
        "List of people who receive email on some application events. "
        "(e.g.: account creation/activation)."),
    category="snf-common-admins",
    export=True,
)

#
# Email server configuration
#

EMAIL_HOST = Default(
    default_value="127.0.0.1",
    description=(
        "IP or domain of the smtp server that will be used by Synnefo."),
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

LOG_DIR = Default(
    default_value="/var/log/synnefo/",
    description=("Directory where log files are saved. "
                 "Currently only snf-manage uses this to "
                 "save the output of the commands being executed."),
    category="snf-common-admins",
)

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
    description=(
        "Email where users can contact for support. Will appear in "
        "emails and UI."),
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

EMAIL_BACKEND = Default(
    default_value='django.core.mail.backends.smtp.EmailBackend',
    description='The backend to use for sending emails.',
    category="snf-webproject-admins",
)

EMAIL_FILE_PATH = Default(
    default_value=None,
    description=(
        "The directory used by the file email backend to store output files."),
    category="snf-webproject-admins",
)
