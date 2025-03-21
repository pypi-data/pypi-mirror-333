# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Utility functions for lmeval. Functions should adapt to the platform.
"""

import os
from pathlib import Path
import re
import shutil
import threading
import time

from lmeval import system_config
from lmeval.logger import log


file_walker = os.walk


def is_google() -> bool:
  return system_config.CONFIG["platform"] == "google"


def match_files(
    base_path: str, pattern: str | re.Pattern[str], file_only: bool = False
) -> list[str]:
  """Glob files recursively starting at base and returns matching paths."""
  log.debug(f"match_files base_path: {base_path}")
  if isinstance(pattern, str):
    pattern = re.compile(pattern)
  else:
    assert isinstance(pattern, re.Pattern)
  paths = []
  for dirname, subdirs, filenames in file_walker(base_path):
    dir_path = Path(dirname)
    for subdir in subdirs:
      path = dir_path / subdir
      path = path.as_posix()
      if not file_only and pattern.match(path):
        paths.append(path)
      paths.extend(match_files(path, pattern))
    for filename in filenames:
      path = dir_path / filename
      path = path.as_posix()
      log.debug(f"match_files visit file: {path}")
      if pattern.match(path):
        paths.append(path)
    return paths


def recursively_copy_dir(src: str, dst: str, overwrite: bool = True,
                         backup: bool = False, remove_backup: bool = True):
  """Recursively copy a directory with an optional temp backup."""
  src = Path(src).as_posix()
  dst = Path(dst).as_posix()
  assert not dst.startswith(src)
  backup_dir = None
  if backup:
    suffix = int(time.time())
    backup_dir = f"{dst}_{suffix}"

  if is_google():
    # Google needs special function for files
    raise NotImplementedError
  else:
    if backup_dir and Path(dst).exists():
      os.rename(dst, backup_dir)
    if overwrite:
      shutil.rmtree(dst)
    Path(dst).mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst)
    if remove_backup and Path(backup_dir).exists():
      shutil.rmtree(backup_dir)


class ReaderWriterLock:
    """A single writer, multipler reader loack."""
    def __init__(self):
        self.lock = threading.Lock()
        self.readers = 0
        self.writers_waiting = 0
        self.cv = threading.Condition(self.lock)

    def acquire_read(self, timeout=None):
        with self.cv:
            end_time = time.time() + timeout if timeout else None
            while self.writers_waiting > 0:
                if timeout:
                    remaining_time = end_time - time.time()
                    if remaining_time <= 0:
                        raise TimeoutError("Timeout acquiring read lock") 
                    self.cv.wait(remaining_time)
                else:
                    self.cv.wait()
            self.readers += 1

    def release_read(self):
        with self.cv:
            self.readers -= 1
            if self.readers == 0:
                self.cv.notify_all()

    def acquire_write(self, timeout=None):
        with self.cv:
            self.writers_waiting += 1
            end_time = time.time() + timeout if timeout else None
            while self.readers > 0 or self.writers_waiting > 1:
                if timeout:
                    remaining_time = end_time - time.time()
                    if remaining_time <= 0:
                        self.writers_waiting -= 1
                        raise TimeoutError("Timeout acquiring write lock") 
                    self.cv.wait(remaining_time)
                else:
                    self.cv.wait()
            self.writers_waiting -= 1

    def release_write(self):
        with self.cv:
            self.cv.notify_all()


class _Reader:
    def __init__(self, lock, timeout=None):
        self.lock = lock
        self.timeout = timeout
    
    def __enter__(self):
        self.lock.acquire_read(self.timeout)
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lock.release_read()


class _Writer:
    def __init__(self, lock, timeout=None):
        self.lock = lock
        self.timeout = timeout
    
    def __enter__(self):
        self.lock.acquire_write(self.timeout)
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lock.release_write()
        

class ReadWriteLock(ReaderWriterLock):
    """Class for using with statement.
    
    usage:
        my_lock = ReadWriteLock()

        with my_lock.read():
          ...

        with my_lock.write():
          ...
    """
    def read(self, timeout=None):
        return _Reader(self, timeout)
    
    def write(self, timeout=None):
        return _Writer(self, timeout)