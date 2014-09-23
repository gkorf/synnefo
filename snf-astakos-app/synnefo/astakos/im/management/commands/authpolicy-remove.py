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

from snf_django.management.commands import SynnefoCommand, CommandError

from synnefo.astakos.im.models import AuthProviderPolicyProfile as Profile


class Command(SynnefoCommand):
    args = "<profile_name>"
    help = "Remove an authentication provider policy"

    option_list = SynnefoCommand.option_list + ()

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Invalid number of arguments")

        try:
            profile = Profile.objects.get(name=args[0])
            profile.delete()
        except Profile.DoesNotExist:
            raise CommandError("Invalid profile name")
