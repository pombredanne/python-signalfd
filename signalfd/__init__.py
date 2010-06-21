# Copyright (c) 2010 Jean-Paul Calderone.
# See LICENSE file for details.

try:
    from signalfd._signalfd import \
        sigprocmask, signalfd, \
        SIG_BLOCK, SIG_UNBLOCK, SIG_SETMASK, \
        SFD_CLOEXEC, SFD_NONBLOCK
except ImportError:
    from _signalfd import \
        sigprocmask, signalfd, \
        SIG_BLOCK, SIG_UNBLOCK, SIG_SETMASK, \
        SFD_CLOEXEC, SFD_NONBLOCK

__all__ = [
    'sigprocmask', 'signalfd',

    'SIG_BLOCK', 'SIG_UNBLOCK', 'SIG_SETMASK',

    'SFD_CLOEXEC', 'SFD_NONBLOCK']
