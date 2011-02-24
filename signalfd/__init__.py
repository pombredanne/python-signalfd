# Copyright (c) 2010 Jean-Paul Calderone.
# See LICENSE file for details.
import os
from operator import itemgetter
import struct

SIGINFO_SZ = 128

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
    return SigInfo(*struct.unpack(siginfo_t, os.read(fd, SIGINFO_SZ)))

class SigInfo(tuple):
        """SigInfo(*fields)

        Class representing signal information
        """

        __slots__ = ()

        _fields = ('ssi_signo', 'ssi_errno', 'ssi_code', 'ssi_pid', 'ssi_uid',
                'ssi_fd', 'ssi_tid', 'ssi_band', 'ssi_overrun', 'ssi_trapno',
                'ssi_status', 'ssi_int', 'ssi_ptr', 'ssi_utime', 'ssi_stime',
                'ssi_addr', 'padding')

        def __new__(cls, ssi_signo, ssi_errno, ssi_code, ssi_pid, ssi_uid,
                ssi_fd, ssi_tid, ssi_band, ssi_overrun, ssi_trapno, ssi_status,
                ssi_int, ssi_ptr, ssi_utime, ssi_stime, ssi_addr, padding):
            return tuple.__new__(cls, (ssi_signo, ssi_errno, ssi_code, ssi_pid,
                ssi_uid, ssi_fd, ssi_tid, ssi_band, ssi_overrun, ssi_trapno,
                ssi_status, ssi_int, ssi_ptr, ssi_utime, ssi_stime, ssi_addr,
                padding))

        @classmethod
        def _make(cls, iterable, new=tuple.__new__, len=len):
            """Make a new SigInfo object from a sequence or iterable"""
            result = new(cls, iterable)
            if len(result) != 17:
                raise TypeError('Expected 17 arguments, got %d' % len(result))
            return result

        def __str__(self):
            return '<SigInfo %d>' % self.ssi_signo

        def __repr__(self):
            return 'SigInfo(ssi_signo=%r, ssi_errno=%r, ssi_code=%r, ssi_pid=%r, ssi_uid=%r, ssi_fd=%r, ssi_tid=%r, ssi_band=%r, ssi_overrun=%r, ssi_trapno=%r, ssi_status=%r, ssi_int=%r, ssi_ptr=%r, ssi_utime=%r, ssi_stime=%r, ssi_addr=%r, padding=%r)' % self

        def _asdict(t):
            """Return a new dict which maps field names to their values"""
            return {'ssi_signo': t[0], 'ssi_errno': t[1], 'ssi_code': t[2], 'ssi_pid': t[3], 'ssi_uid': t[4], 'ssi_fd': t[5], 'ssi_tid': t[6], 'ssi_band': t[7], 'ssi_overrun': t[8], 'ssi_trapno': t[9], 'ssi_status': t[10], 'ssi_int': t[11], 'ssi_ptr': t[12], 'ssi_utime': t[13], 'ssi_stime': t[14], 'ssi_addr': t[15], 'padding': t[16]}

        def _replace(self, **kwds):
            'Return a new SigInfo object replacing specified fields with new values'
            result = self._make(map(kwds.pop, ('ssi_signo', 'ssi_errno',
                'ssi_code', 'ssi_pid', 'ssi_uid', 'ssi_fd', 'ssi_tid',
                'ssi_band', 'ssi_overrun', 'ssi_trapno', 'ssi_status',
                'ssi_int', 'ssi_ptr', 'ssi_utime', 'ssi_stime', 'ssi_addr',
                'padding'), self))
            if kwds:
                raise ValueError('Got unexpected field names: %r' % kwds.keys())
            return result

        def __getnewargs__(self):
            return tuple(self)

        ssi_signo = property(itemgetter(0), doc='Signal number')
        ssi_errno = property(itemgetter(1), doc='Error number (unused)')
        ssi_code = property(itemgetter(2),  doc='Signal code')
        ssi_pid = property(itemgetter(3),   doc='PID of sender')
        ssi_uid = property(itemgetter(4),   doc='Real UID of sender')
        ssi_fd = property(itemgetter(5),    doc='File descriptor (SIGIO)')
        ssi_tid = property(itemgetter(6),   doc='Kernel timer ID')
        ssi_band = property(itemgetter(7),  doc='Band event (SIGIO)')
        ssi_overrun = property(itemgetter(8), doc='POSIX timer overrun count')
        ssi_trapno = property(itemgetter(9),  doc='Trap number')
        ssi_status = property(itemgetter(10),
                doc='Exit status or signal (SIGCHLD)')
        ssi_int = property(itemgetter(11),  doc='Integer sent by sigqueue')
        ssi_ptr = property(itemgetter(12),  doc='Pointer sent by sigqueue')
        ssi_utime = property(itemgetter(13),
                doc='User CPU time consumed (SIGCHLD)')
        ssi_stime = property(itemgetter(14),
                doc='System CPU time consumed (SIGCHLD)')
        ssi_addr = property(itemgetter(15), doc='Address that generated '
                'signal (for hardware generated signals)')
        padding = property(itemgetter(16),  doc='Pad size to 128 bytes')


siginfo_t = (
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
