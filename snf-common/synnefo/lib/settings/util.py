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

from synnefo.lib.settings.setup import NoValue, SettingsError


def auto_configure_default_from_dep(setting, value, deps):
    """If no value was given by the user, set the value to that
       of the depenency (must be dependent to a single setting).

    """
    if value is not NoValue:
        # acknowledge user-provided setting
        return NoValue

    if len(deps) != 1:
        m = ("The callback of setting '{name}' requires the setting to "
             "have exactly one dependency, not {n}.")
        m = m.format(name=setting.setting_name, n=len(deps))
        raise SettingsError(m)

    return deps.values()[0]
