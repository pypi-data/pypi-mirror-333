from .archive import Archive
from .crypto import encrypt_data, decrypt_data
def test_encryption(tmp_path_factory):
    keyset = Archive.KEYSET_STR
    "test encryption"
    data = b"Hello World"
    encrypted_data = encrypt_data(data, keyset_str=keyset)
    decrypted_data = decrypt_data(encrypted_data, keyset_str=keyset)
    assert data == decrypted_data