#!/bin/sh
#
#  This is a simple wrapper to run the
#  python code in python/.
#
SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
python $SCRIPTPATH/inkpulp-quota.pyo $@

# EOF
