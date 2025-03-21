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

import tink
from tink import aead, secret_key_access

aead.register()

def get_handle(keyset_str: str):
    """Return a tink keyset handle to encrypt and decrypt data"""
    kh = tink.json_proto_keyset_format.parse(keyset_str, secret_key_access.TOKEN)
    return kh.primitive(aead.Aead)

def encrypt_data(plaintext: bytes, keyset_str: str) -> bytes:
    """Encrypts the data using the provided key."""
    primitive = get_handle(keyset_str)
    return primitive.encrypt(plaintext, associated_data=b'not a security feature')

def decrypt_data(ciphertext: bytes, keyset_str: str) -> bytes:
    """Decrypts the data using the provided key."""
    primitive = get_handle(keyset_str)
    return primitive.decrypt(ciphertext, associated_data=b'not a security feature')
