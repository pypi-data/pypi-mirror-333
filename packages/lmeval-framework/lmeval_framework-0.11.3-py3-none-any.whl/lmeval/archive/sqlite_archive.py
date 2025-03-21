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

import sqlite3
import time
import zlib
import tempfile
import logging

from lmeval import system_config
from lmeval import utils
from lmeval.archive.archive import Archive, FileInfo

logger = logging.getLogger(__name__)


class SQLiteArchive(Archive):
    """
    SQLite-based archive for storing data with optional encryption and compression.

    This class provides functionality to write, read, and list files stored within
    an SQLite database. It supports optional encryption and compression of the data
    and can be configured to use temporary files for increased safety.
    """

    def __init__(self, path,
                 compression_level: int = -1,
                 keyfname: str = 'key',
                 use_tempfile: bool | None = None,
                 restore: bool = True):
        super().__init__(name="SQLiteArchive", version="1.0")
        self._init_paths_and_temp_dir(path, use_tempfile, restore)

        try:
            with self.conn:  # Use context manager for connection
                self._create_table_and_index()
        except sqlite3.OperationalError as e:
            raise ValueError( f"Error opening or initializing SQLite archive at {self.path}: {e}") from e

        self.compression_level = compression_level
        self.keyfname = keyfname
        self.key = ""

    def _init_paths_and_temp_dir(self, path, use_tempfile, restore):
        """Initializes paths and temporary directory based on configuration."""
        self.temp_dir = None
        if use_tempfile is None:
            use_tempfile = system_config.CONFIG.get("use_tempfile", False)
        if use_tempfile:
            self.temp_dir = tempfile.TemporaryDirectory()
            self.path = self.temp_dir.name + "/data.db"
            self.real_path = path
            p = utils.Path(self.real_path)
            if restore and p.exists():
                utils.recursively_copy_dir(self.real_path, self.path,
                                           overwrite=True)
        else:
            self.path = path
            self.real_path = None
            p = utils.Path(self.path)
            if not p.parent.exists():
                p.parent.mkdir(parents=True)
        self.path = str(self.path)
        print(f"self.path: {self.path}")
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()

    def _create_table_and_index(self):
        """Creates the files table and index if they don't exist."""
        # Check if the table already exists
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='files'")
        table_exists = self.cursor.fetchone() is not None

        if not table_exists:
            self.cursor.execute('''
                CREATE TABLE files (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    data BLOB NOT NULL,
                    size INTEGER NOT NULL,
                    encrypted BOOLEAN NOT NULL,
                    compressed BOOLEAN NOT NULL,
                    update_time INTEGER,
                    hash TEXT,
                    filetype TEXT,
                    modality TEXT
                );
            ''')

        # Check if the index already exists
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_file_name'"
        )
        index_exists = self.cursor.fetchone() is not None

        if not index_exists:
            self.cursor.execute('''
                CREATE INDEX idx_file_name ON files (name);
            ''')
        self.conn.commit()

    def close(self):
        """Closes the database connection and cleans up the temporary directory."""
        if self.conn:
            self.persist()
            self.conn.close()
            if self.temp_dir is not None:
                self.temp_dir.cleanup()

    def write(self, name: str, data: bytes | str, encrypted: bool,
              compress: bool = True, file_type: str = "",
              modality: str = ""):
        if isinstance(data, str):
            data = data.encode("utf-8")

        if compress:
            compressed_data = zlib.compress(data, level=self.compression_level)
        else:
            compressed_data = data

        if encrypted:
            compressed_data = self._encrypt_data(compressed_data)

        file_hash = self._compute_hash(data)
        size = len(data)

        try:
            with self.conn:  # Use context manager for transaction
                self.cursor.execute(
                    "INSERT INTO files (name, data, size, encrypted, compressed, update_time, hash, filetype, modality) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (name, compressed_data,  size, encrypted, compress,
                     int(time.time()), file_hash, file_type, modality))
        except sqlite3.IntegrityError:
            # Handle the case where the file name already exists (unique constraint)
            logger.warning(
                f"File '{name}' already exists in the archive. Updating...")
            with self.conn:  # Use context manager for transaction
                self.cursor.execute(
                    "UPDATE files SET data = ?, size= ?, encrypted = ?, compressed = ?, update_time = ?, hash = ?, filetype = ?, modality = ? WHERE name = ?",
                    (compressed_data, size, encrypted, compress, int(time.time()),
                     file_hash, file_type, modality, name))

    def read(self, name: str) -> bytes | str:
        with self.conn:
            self.cursor.execute(
                "SELECT data, encrypted, compressed FROM files WHERE name = ?",
                (name,))
            row = self.cursor.fetchone()

        if row is None:
            return ""

        data, encrypted, compressed = row

        if encrypted:
            data = self._decrypt_data(data)

        if compressed:
            data = zlib.decompress(data)

        return data

    def files_info(self) -> list[FileInfo]:
        "Return the list of files alongside their metadata"
        files = []
        with self.conn:
            self.cursor.execute("SELECT id, name, size, encrypted, compressed, update_time, hash, filetype, modality FROM files")
            for row in self.cursor.fetchall():
                id, name, size, encrypted, compressed, update_time, hash, filetype, modality = row
                finfo = FileInfo(id=id,
                         name=name, size=size, compressed=compressed, encrypted=encrypted, update_time=update_time, hash=hash,
                         filetype=filetype, modality=modality)

                files.append(finfo)
        return files

    def _get_keyset(self) -> str:
        "read encryption key from archive and returns it"
        if self.key:
            return self.key

        # try to get the key from db
        key = self.read(self.keyfname)
        if key:
            self.key = key
        else:
            # If the key is not in the archive, write it
            if not self.KEYSET_STR:
                raise ValueError("No key found in archive and self.KEYSET_STR is not set")

            key = self.KEYSET_STR
            self.write(self.keyfname, key, encrypted=False, compress=True, file_type="json", modality="data")
            self.key = key

        return self.key



        return self.key

    def persist(self):
        "persist the archive to the 'real_path'"
        if self.real_path is not None:
            self.conn.commit()  # Ensure changes are committed
            p = utils.Path(self.real_path)
            if not p.exists():
                p.mkdir(parents=True)
            utils.recursively_copy_dir(self.path, self.real_path,
                                       overwrite=True, backup=True)

