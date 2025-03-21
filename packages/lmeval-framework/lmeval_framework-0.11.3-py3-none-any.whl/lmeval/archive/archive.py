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

import abc
from hashlib import blake2b
from .crypto import encrypt_data, decrypt_data

# use orjson if available faster!
try:
    import orjson as json
except ImportError:
    import json

from ..custom_model import CustomModel


class FileInfo(CustomModel):
    "FileInfo represents archive file metadata"
    id: int
    name: str
    size: int
    encrypted: bool
    compressed: bool
    update_time: int
    hash: str
    modality: str
    filetype: str



class Archive(abc.ABC):
    """
    Notes:
        - The serializer track the files integrity and encryption status so there
        is no need for the user to know which one should be decrypted when reading.
        This is only decided when writing to the archive.

        - When selecting technology we are looking at:
            - replacement in place of files to avoid massive data copy and allows update
            - Support of multifiles so we can include the media in the benchmark at least locally

    """

    KEYSET_STR = r"""{
        "key": [{
            "keyData": {
                "keyMaterialType": "SYMMETRIC",
                "typeUrl": "type.googleapis.com/google.crypto.tink.AesGcmKey",
                "value": "GiBWyUfGgYk3RTRhj/LIUzSudIWlyjCftCOypTr0jCNSLg=="
            },
            "keyId": 294406504,
            "outputPrefixType": "TINK",
            "status": "ENABLED"
        }],
        "primaryKeyId": 294406504
    }"""

    def __init__(self, name: str, version: str) -> None:
        super().__init__()
        self.name = name
        self.version = version

    def version_string(self) -> str:
        return f"{self.name}-{self.version}".replace(' ', '_').lower().strip()

    @abc.abstractmethod
    def read(self, name: str) -> bytes:
        pass

    def read_json(self, name: str):
        data = self.read(name).decode()
        return json.loads(data)

    def write_json(self, name: str, value, encrypted: bool = True):
        data = json.dumps(value)
        self.write(name, data, encrypted, file_type="json", modality="data")

    @abc.abstractmethod
    def write(self, name: str, value: str| bytes, encrypted: bool = True,
              file_type: str = "", modality: str = ""):
        pass

    @abc.abstractmethod
    def files_info(self) -> list[FileInfo]:
        "return files metadata"
        pass

    @abc.abstractmethod
    def _get_keyset(self) -> str:
        "get the keyset used for encryption"
        pass

    def _encrypt_data(self, plaintext: bytes) -> bytes:
        keyset = self._get_keyset()
        return encrypt_data(plaintext, keyset)

    def _decrypt_data(self, ciphertext: bytes) -> bytes:
        keyset = self._get_keyset()
        return decrypt_data(ciphertext, keyset)

    def _compute_hash(self, data: bytes|str, digest_size: int = 16) -> str:
        "compute data hash for integrity manifest"
        h = blake2b(digest_size=digest_size)
        h.update(data)
        return h.hexdigest()

