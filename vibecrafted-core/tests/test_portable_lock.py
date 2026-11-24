"""Windows lock-region creation must survive a peer that already locked byte 0."""

from __future__ import annotations

import importlib.util
import os
import sys
import types
from pathlib import Path

import pytest
from vibecrafted_core import portable_lock


def _open(path: Path) -> int:
    return os.open(path, os.O_RDWR | os.O_CREAT, 0o600)


def test_non_empty_lock_file_is_ready_without_writing(tmp_path, monkeypatch):
    path = tmp_path / "ledger.lock"
    path.write_bytes(b"\n")
    fd = _open(path)
    try:

        def _no_write(*_args):
            raise AssertionError("a ready lock file must not be written")

        monkeypatch.setattr(portable_lock.os, "write", _no_write)
        portable_lock._ensure_lock_region(fd)
    finally:
        os.close(fd)
    assert path.read_bytes() == b"\n"


def test_peer_holding_the_lock_byte_is_tolerated(tmp_path, monkeypatch):
    path = tmp_path / "ledger.lock"
    fd = _open(path)
    try:

        def _peer_won(_fd, _data):
            # The peer created and locked byte 0 between our stat and write.
            path.write_bytes(b"\n")
            raise PermissionError(13, "Permission denied")

        monkeypatch.setattr(portable_lock.os, "write", _peer_won)
        portable_lock._ensure_lock_region(fd)
        assert os.lseek(fd, 0, os.SEEK_CUR) == 0
    finally:
        os.close(fd)
    assert path.read_bytes() == b"\n"


def test_permission_error_on_empty_file_is_not_swallowed(tmp_path, monkeypatch):
    path = tmp_path / "ledger.lock"
    fd = _open(path)
    try:

        def _denied(_fd, _data):
            raise PermissionError(13, "Permission denied")

        monkeypatch.setattr(portable_lock.os, "write", _denied)
        with pytest.raises(PermissionError):
            portable_lock._ensure_lock_region(fd)
    finally:
        os.close(fd)


def test_empty_lock_file_gets_one_byte(tmp_path):
    path = tmp_path / "ledger.lock"
    fd = _open(path)
    try:
        portable_lock._ensure_lock_region(fd)
    finally:
        os.close(fd)
    assert path.read_bytes() == b"\n"


def _load_windows_shape(monkeypatch) -> tuple[types.ModuleType, list[tuple]]:
    calls: list[tuple] = []
    fake = types.ModuleType("msvcrt")
    fake.LK_UNLCK, fake.LK_LOCK, fake.LK_NBLCK = 0, 1, 2
    fake.locking = lambda fd, mode, nbytes: calls.append((fd, mode, nbytes))
    monkeypatch.setitem(sys.modules, "msvcrt", fake)
    real_name = os.name
    monkeypatch.setattr(os, "name", "nt")
    spec = importlib.util.spec_from_file_location(
        "_portable_lock_windows_shape", portable_lock.__file__
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(os, "name", real_name)
    return module, calls


def test_windows_flock_waits_on_a_peer_created_lock_byte(tmp_path, monkeypatch):
    module, calls = _load_windows_shape(monkeypatch)
    path = tmp_path / "ledger.lock"
    fd = _open(path)
    try:

        def _peer_won(_fd, _data):
            path.write_bytes(b"\n")
            raise PermissionError(13, "Permission denied")

        monkeypatch.setattr(module.os, "write", _peer_won)
        module.flock(fd, module.LOCK_EX)
        module.flock(fd, module.LOCK_UN)
    finally:
        monkeypatch.undo()
        os.close(fd)
    assert calls == [(fd, 1, 1), (fd, 0, 1)]
