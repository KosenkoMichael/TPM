import pytest

from unittest.mock import patch, MagicMock
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import (
    Cipher,
    algorithms,
)
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

from algoritms.symmetric_cipher import Symmetric


@pytest.fixture
def symmetric_key() -> bytes:
    """
    Fixture to generate a symmetric key.

    Returns:
        bytes: A 32-byte symmetric key.
    """
    return Symmetric.generate_key(32)


@pytest.fixture
def nonce() -> bytes:
    """
    Fixture to generate a nonce.

    Returns:
        bytes: A 16-byte nonce.
    """
    return Symmetric.generate_key(16)


def test_keys(symmetric_key: bytes, nonce: bytes) -> None:
    """
    Test the generation of symmetric key and nonce.

    Args:
        symmetric_key (bytes): The symmetric key generated by the fixture.
        nonce (bytes): The nonce generated by the fixture.

    Raises:
        AssertionError: If any of the assertions fail.
    """
    assert len(symmetric_key) == 32, "Symmetric key's len must be 32"
    assert len(nonce) == 16, "nonce's len must be 16"
    assert isinstance(symmetric_key, bytes), "Symmetric key's type must be bytes"
    assert isinstance(nonce, bytes), "nonce's type must be bytes"


@patch("algoritms.serialization.Serialization.serialize_symmetric_key")
@patch("algoritms.functional.Functional.read_file")
@patch("algoritms.serialization.Serialization.deserialize_symmetric_key")
@patch("algoritms.functional.Functional.write_file_bytes")
def test_encrypt(
    mock_write_file_bytes: MagicMock,
    mock_deserialize_symmetric_key: MagicMock,
    mock_read_file: MagicMock,
    mock_serialize_symmetric_key: MagicMock,
    symmetric_key: bytes,
) -> None:
    """
    Test the encryption functionality of the Symmetric class.

    Args:
        mock_write_file_bytes (MagicMock): Mock for writing encrypted file bytes.
        mock_deserialize_symmetric_key (MagicMock): Mock for deserializing symmetric key.
        mock_read_file (MagicMock): Mock for reading the input text file.
        mock_serialize_symmetric_key (MagicMock): Mock for serializing the nonce.
        symmetric_key (bytes): The symmetric key used for encryption.

    Raises:
        AssertionError: If any of the assertions fail.
    """
    text_to_encrypt = "Any test message"

    mock_read_file.return_value = text_to_encrypt
    mock_deserialize_symmetric_key.return_value = symmetric_key
    mock_serialize_symmetric_key.return_value = None

    Symmetric.encrypt(
        "text/to/cipher", "path/to/symmetric_origin", "path/to/nonce", "encrypted/path"
    )

    mock_write_file_bytes.assert_called_once()
    encrypted_text: bytes = mock_write_file_bytes.call_args[0][1]
    nonce: bytes = mock_serialize_symmetric_key.call_args[0][1]

    cipher = Cipher(
        algorithms.ChaCha20(symmetric_key, nonce),
        mode=None,
        backend=default_backend(),
    )
    decryptor = cipher.decryptor()
    decrypted_text = decryptor.update(encrypted_text) + decryptor.finalize()
    unpadder = padding.PKCS7(256).unpadder()
    unpadded_dc_text = unpadder.update(decrypted_text) + unpadder.finalize()
    dec_unpad_text = unpadded_dc_text.decode("UTF-8")

    assert text_to_encrypt == dec_unpad_text, "Decrypted text does not match the original text"


@patch("algoritms.serialization.Serialization.deserialize_symmetric_key")
@patch("algoritms.functional.Functional.read_file_bytes")
@patch("algoritms.functional.Functional.write_file")
def test_decrypt(
    mock_write_file: MagicMock,
    mock_read_file_bytes: MagicMock,
    mock_deserialize_symmetric_key: MagicMock,
    symmetric_key: bytes,
    nonce: bytes,
) -> None:
    """
    Test the decryption functionality of the Symmetric class.

    Args:
        mock_write_file (MagicMock): Mock for writing the decrypted text to a file.
        mock_read_file_bytes (MagicMock): Mock for reading file bytes (nonce and encrypted text).
        mock_deserialize_symmetric_key (MagicMock): Mock for deserializing symmetric key.
        symmetric_key (bytes): The symmetric key used for decryption.
        nonce (bytes): The nonce used for decryption.

    Raises:
        AssertionError: If any of the assertions fail.
    """
    origin_text = "Any test message"
    cipher = Cipher(
        algorithms.ChaCha20(symmetric_key, nonce),
        None,
        backend=default_backend()
    )
    padder = padding.PKCS7(256).padder()
    text_to_bytes = bytes(origin_text, "UTF-8")
    padded_text = padder.update(text_to_bytes) + padder.finalize()
    encryptor = cipher.encryptor()
    encrypted_text = encryptor.update(padded_text) + encryptor.finalize()

    mock_read_file_bytes.side_effect = [nonce, encrypted_text]
    mock_deserialize_symmetric_key.return_value = symmetric_key

    Symmetric.decrypt(
        "path/to/symmetric", "path/to/nonce", "path/to/encrypted", "path/to/decrypted"
    )

    mock_write_file.assert_called_once()
    decrypted_text: str = mock_write_file.call_args[0][1]

    assert decrypted_text == origin_text, "Decrypted text does not match the original text"
