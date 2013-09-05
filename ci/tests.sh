#!/bin/sh
set -e

if [ -z "${SYNNEFO_TEST_SETTINGS_DIR}" ]; then
    SYNNEFO_TEST_SETTINGS_DIR="/etc/synnefo-test-settings"
fi
export SYNNEFO_SETTINGS_DIR="${SYNNEFO_TEST_SETTINGS_DIR}"

SNF_MANAGE=$(which snf-manage) ||
	{ echo "Cannot find snf-manage in $PATH" 1>&2; exit 1; }

runtest () {
    TEST="$SNF_MANAGE test $* --traceback --noinput --settings=synnefo.settings"

    runCoverage "$TEST"
}

runCoverage () {
    if coverage >/dev/null 2>&1; then
      coverage run $1
      coverage report --include=snf-*
    else
      echo "WARNING: Cannot find coverage in path, skipping coverage tests" 1>&2
      $1
    fi
}

export ASTAKOS_BASE_URL='https://astakos.example.synnefo.org/accounts'
export CYCLADES_BASE_URL='https://cyclades.example.synnefo.org/compute'
export PITHOS_BASE_URL='https://pithos.example.synnefo.org/object-store'

ASTAKOS_APPS="im quotaholder_app oa2"
CYCLADES_APPS="api db logic plankton quotas vmapi helpdesk userdata"
PITHOS_APPS="api"

TEST_COMPONENTS="$@"
if [ -z "$TEST_COMPONENTS" ]; then
    TEST_COMPONENTS="astakos cyclades pithos astakosclient"
fi

for component in $TEST_COMPONENTS; do
    if [ "$component" = "astakos" ]; then
        runTest $ASTAKOS_APPS
    elif [ "$component" = "cyclades" ]; then
        export SYNNEFO_EXCLUDE_PACKAGES="snf-pithos-app"
        runTest $CYCLADES_APPS
    elif [ "$component" = "pithos" ]; then
        export SYNNEFO_EXCLUDE_PACKAGES="snf-cyclades-app"
        runTest $PITHOS_APPS
    elif [ "$component" = "astakosclient" ]; then
        TEST="nosetests astakosclient"
        runCoverage "$TEST"
    fi
done
