# Copyright (c) 2010 Jean-Paul Calderone.
# Copyright (c) 2011 Michael Schurter <michael@susens-schurter.com>
# See LICENSE file for details.
import os
import struct

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

__version__ = '0.2'
__version_info__ = (0, 2)

__all__ = [
    'created_signalfd', 'read_signalfd', 'siginfo_t', 'SigInfo',

    'sigprocmask', 'signalfd',

    'SIG_BLOCK', 'SIG_UNBLOCK', 'SIG_SETMASK',

    'SFD_CLOEXEC', 'SFD_NONBLOCK',

    '__version__', '__version_info__']

_signo_to_str = {
        1: 'SIGHUP',
        2: 'SIGINT',
        3: 'SIGQUIT',
        4: 'SIGILL',
        5: 'SIGTRAP',
        6: 'SIGABRT',
        7: 'SIGBUS',
        8: 'SIGFPE',
        9: 'SIGKILL',
        10: 'SIGUSR1',
        11: 'SIGSEGV',
        12: 'SIGUSR2',
        13: 'SIGPIPE',
        14: 'SIGALRM',
        15: 'SIGTERM',
        16: 'SIGSTKFLT',
        17: 'SIGCHLD',
        18: 'SIGCONT',
        19: 'SIGSTOP',
        20: 'SIGTSTP',
        21: 'SIGTTIN',
        22: 'SIGTTOU',
        23: 'SIGURG',
        24: 'SIGXCPU',
        25: 'SIGXFSZ',
        26: 'SIGVTALRM',
        27: 'SIGPROF',
        28: 'SIGWINCH',
        29: 'SIGIO',
        30: 'SIGPWR',
        31: 'SIGSYS',
        34: 'SIGRTMIN',
        64: 'SIGRTMAX',
    }

def create_signalfd(signals, flags=0):
    """Creates a new signal file descriptor

    Shortcut for:
        signalfd.sigprocmask(signalfd.SIG_BLOCK, signals)
        signalfd(-1, signals, flags)
    """
    sigprocmask(SIG_BLOCK, signals)
    return signalfd(-1, signals, flags)

def read_signalfd(fd):
    """Given a signalfd, return a SigInfo instance"""
    return SigInfo(os.read(fd, siginfo_t.size))

class SigInfo(object):
    def __init__(self, data):
        (self.ssi_signo,
        self.ssi_errno,
        self.ssi_code,
        self.ssi_pid,
        self.ssi_uid,
        self.ssi_fd,
        self.ssi_tid,
        self.ssi_band,
        self.ssi_overrun,
        self.ssi_trapno,
        self.ssi_status,
        self.ssi_int,
        self.ssi_ptr,
        self.ssi_utime,
        self.ssi_stime,
        self.ssi_addr,
        self.padding) = siginfo_t.unpack(data)

    @property
    def signo(self):
        return self.ssi_signo

    @property
    def signal(self):
        return _signo_to_str[self.ssi_signo]

    def __str__(self):
        return self.signal

siginfo_t = struct.Struct(
        'I' # ssi_signo   - Signal number
        'i' # ssi_errno   - Error number (unused)
        'i' # ssi_code    - Signal code
        'I' # ssi_pid     - PID of sender
        'I' # ssi_uid     - Real UID of sender
        'i' # ssi_fd      - File descriptor (SIGIO)
        'I' # ssi_tid     - Kernel timer ID (POSIX timers)
        'I' # ssi_band    - Band event (SIGIO)
        'I' # ssi_overrun - POSIX timer overrun count
        'I' # ssi_trapno  - Trap number that caused signal
        'i' # ssi_status  - Exit status or signal (SIGCHLD)
        'i' # ssi_int     - Integer sent by sigqueue (2)
        'Q' # ssi_ptr     - Pointer sent by sigqueue (2)
        'Q' # ssi_utime   - User CPU time consumed (SIGCHLD)
        'Q' # ssi_stime   - System CPU time consumed (SIGCHLD)
        'Q' # ssi_addr    - Address that generated signal
            #               (for hardware generated signals)
        '48s' # pad[X]    - Pad size to 128 bytes for future use
    )
