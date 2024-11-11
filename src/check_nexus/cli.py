"""
Command line interface
"""

import sys
from . import check_metadata, validate_nexus, set_logging_level


def run_check(*args):
    """argument runner for check_nexus"""
    tot = 0
    if '--info' in args:
        set_logging_level('info')
    if '--debug' in args:
        set_logging_level('debug')

    for n, arg in enumerate(args):
        if arg == '-h' or arg.lower() == '--help' or arg == 'man':
            tot += 1
            import check_nexus
            help(check_nexus)
        if arg.endswith('.nxs'):
            tot += 1
            check_metadata(arg)

    if tot > 0:
        print('\nCompleted')
    else:
        import check_nexus
        help(check_nexus)


def cli_checknexus():
    """command line argument"""
    run_check(*sys.argv)


def run_validate(*args):
    """argument runner for validator"""
    tot = 0
    for n, arg in enumerate(args):
        if arg == '-h' or arg.lower() == '--help' or arg == 'man':
            tot += 1
            import check_nexus
            help(check_nexus)
        if arg.endswith('.nxs'):
            tot += 1
            validate_nexus(arg)

    if tot > 0:
        print('\nCompleted')
    else:
        import check_nexus
        help(check_nexus)


def cli_validate_nexus():
    """command line argument"""
    run_validate(*sys.argv)
