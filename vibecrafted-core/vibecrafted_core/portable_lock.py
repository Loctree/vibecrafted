"""Advisory file locks that work on POSIX ``fcntl.flock`` and Windows ``msvcrt``.

Installer, control plane, and server supervisor import this module as a
fcntl-shaped object so the same lock grammar runs on Windows without a second
locking system. Shared locks are exclusive on Windows (msvcrt has no reader
lock); that is fail-closed, not a weaker lock.
"""

from __future__ import annotations

import errno
import os

LOCK_SH = 1
LOCK_EX = 2
LOCK_NB = 4
LOCK_UN = 8
F_GETFD = 1
F_SETFD = 2
FD_CLOEXEC = 1


def _ensure_lock_region(fd: int) -> None:
    """Make sure byte 0 exists so ``msvcrt.locking`` has a region to lock.

    A non-empty file is already ready. When several processes race to create
    the byte, the winner may lock it before a peer's write lands; Windows then
    rejects that write with ``PermissionError``. The byte exists by then, so a
    peer only needs to fall through and let the blocking lock call wait.
    """
    if os.fstat(fd).st_size > 0:
        return
    position = os.lseek(fd, 0, os.SEEK_CUR)
    try:
        os.lseek(fd, 0, os.SEEK_END)
        os.write(fd, b"\n")
    except PermissionError:
        if os.fstat(fd).st_size > 0:
            return
        raise
    finally:
        os.lseek(fd, position, os.SEEK_SET)


if os.name != "nt":
    import fcntl as _fcntl

    LOCK_SH = _fcntl.LOCK_SH
    LOCK_EX = _fcntl.LOCK_EX
    LOCK_NB = _fcntl.LOCK_NB
    LOCK_UN = _fcntl.LOCK_UN
    F_GETFD = _fcntl.F_GETFD
    F_SETFD = _fcntl.F_SETFD
    FD_CLOEXEC = _fcntl.FD_CLOEXEC
    flock = _fcntl.flock
    fcntl = _fcntl.fcntl
else:
    import msvcrt

    def flock(fd: int, operation: int) -> None:
        """Lock ``fd`` with flock-shaped flags using ``msvcrt.locking``."""
        if operation & LOCK_UN:
            mode = msvcrt.LK_UNLCK
            nonblocking = False
        elif operation & LOCK_NB:
            mode = msvcrt.LK_NBLCK
            nonblocking = True
        else:
            mode = msvcrt.LK_LOCK
            nonblocking = False
        _ensure_lock_region(fd)
        position = os.lseek(fd, 0, os.SEEK_CUR)
        try:
            os.lseek(fd, 0, os.SEEK_SET)
            msvcrt.locking(fd, mode, 1)
        except OSError as exc:
            if nonblocking:
                raise BlockingIOError(
                    errno.EWOULDBLOCK, "resource temporarily unavailable"
                ) from exc
            raise
        finally:
            os.lseek(fd, position, os.SEEK_SET)

    def fcntl(fd: int, cmd: int, arg: int = 0) -> int:
        """No-op CLOEXEC helper: Windows handle inheritance is process-creation flags."""
        if cmd == F_GETFD:
            return FD_CLOEXEC
        if cmd == F_SETFD:
            return arg
        raise OSError(errno.EINVAL, f"unsupported fcntl command on Windows: {cmd}")
