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
import tempfile
import os
import pytest
from time import time
from lmeval.archive.sqlite_archive import SQLiteArchive


@pytest.fixture
def archive():
    temp_dir = tempfile.TemporaryDirectory()
    db_path = os.path.join(temp_dir.name, "test.db")
    archive = SQLiteArchive(db_path)
    yield archive
    archive.close()
    temp_dir.cleanup()


def test_storage(archive):
    # not encrypted but compressed
    data = b"Hello World"
    archive.write("data", data, encrypted=False, compress=True)
    data2 = archive.read("data")
    assert data == data2

    # encrypted and compressed
    data = b"Hello World"
    archive.write("data", data, encrypted=True, compress=True)
    data2 = archive.read("data")
    assert data == data2

def test_init_creates_table_and_index(archive):
    # Check if the files table exists
    with sqlite3.connect(archive.path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='files';")
        assert cursor.fetchone() is not None

    # Check if the index exists
    with sqlite3.connect(archive.path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_file_name';")
        assert cursor.fetchone() is not None


def test_list_info(archive):
    archive.write("file1", b"data1", encrypted=False, compress=False, file_type='txt', modality='text')
    archive.write("file2", b"data2", encrypted=False, compress=False, file_type='txt', modality='text'  )

    files = archive.files_info()
    assert len(files) == 2
    for f in files:
        assert f.name in ["file1", "file2"]
        assert f.encrypted == False
        assert f.compressed == False
        assert f.filetype == "txt"
        assert f.modality == "text"


def test_write_update_existing_file(archive):
    data1 = b"test data 1"
    data2 = b"test data 2"
    archive.write("test_file", data1, encrypted=False, compress=False)
    archive.write("test_file", data2, encrypted=False, compress=False)

    read_data = archive.read("test_file")
    assert data2 == read_data  # Should be the updated data
