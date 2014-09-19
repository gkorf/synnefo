New settings mechanism
^^^^^^^^^^^^^^^^^^^^^^

Overview
========

We need a framework that would allow the developer to write well structured
settings and assist the admin to give appropriate values, verify that
everything is set correctly, and easily view changes.

Settings Definition
===================

The framework will reside in synnefo.lib.settings of package snf-common.
This will define certain types of settings:
 - Mandatory: must be configured by the admin
 - SubMandatory: is made mandatory if a condition is true
 - Default: provides a default, can be set by the admin
 - Constant: like default, not visible or configurable by the admin
 - Auto: automatically computed, admin may override them
 - Deprecated: must be removed, renamed, or otherwise fixed

Each setting definition must include a description, an example value, and a
category for grouping purposes. In may also declare a dependency on other
settings and use configure_callback to specify a function for configuring a
setting based on the dependencies.

Runtime
=======

When a system goes live, the following things happen:

 1) Settings declared by each package are loaded through their entry point
 `default_settings`. Checks are performed on the well-formedness of the
 declarations and on possible duplicates.

 2) Preconfiguration: based on their dependencies, their relative depth is
 determined.

 3) Loading of configuration files; sets setting.configured_value.

 4) Configuration of settings: recursively follows dependencies, calls
 configure_callback and sets setting.runtime_value. Configuration will fail
 if a Mandatory setting is not configured.

 5) Runtime values bound to setting names are copied to synnefo.settings,
 where they can be found by the django settings mechanism.


Settings management
===================

Management command ``snf-manage settings`` will be provided to query
settings.


Making configuration files
==========================

There are three approaches to that:

a) Delay file creation until deploy time when all packages are installed and
a script is called to make the files; drawback: we would have to handle
diffs ourselves, better off to let (debian) package manager to do the job.

b) Make the files at the package building process and put them in the
package; drawback: builder now needs to load synnefo code that possibly
bring along some extra dependencies.

c) Provide a tool for the developer to create/update the conf files and
commit them, just like we do with django migrations; drawback: overhead on
the developer's side.

Note: We need to support settings depending on other package's settings. For
example, ASTAKOS_IM_STATIC_URL depends on MEDIA_URL from snf-webproject. As
a result determining the numbering of conf files cannot be done at the
package level -- it has to be done synnefo-wide.

We propose a solution based on the third approach: a python script will be
provided (possibly at the root of the Synnefo repo), which will execute the
first two steps of the runtime process, form the conf files based on the
settings' declared categories and the computed depths, and store them under
<package>/conf/.

The script will work by adding the packages from the repo in the python path
and load the settings declarations from the respective packages. The
location of the declarations will be factored out from the entry points
mechanism of setup.py into a <package>/default_settings_path file.

Open issues
===========

Care should be taken that a setting is declared in the appropriate package
and has a unique name synnefo-wide.

Currently, the following settings are duplicates: ASTAKOS_AUTH_URL (provided
by astakos and cyclades, used in snf-django-lib); EXCHANGE_GANETI and
BACKEND_PREFIX_ID (provided by cyclades app and gtools); AMQP_HOSTS and
AMQP_BACKEND (provided by cyclades app and gtools, used in snf-common).

In order to resolve these clashes, we need to check if a certain setting
should be actually unique, shared by multiple packages, or in the other hand
whether it is meaningful for two packages to set differing values -- in that
case we need to split it to separate settings defined in the respective
projects.
