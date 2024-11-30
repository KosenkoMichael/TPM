import pytest

from unittest.mock import patch, MagicMock
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

from algoritms.asymmetric_cipher import Asymmetric


@pytest.fixture
def key_pair() -> tuple[rsa.RSAPublicKey, rsa.RSAPrivateKey]:
    """
    Fixture to generate a pair of RSA keys (public and private).

    Returns:
        tuple: A tuple containing the public key and private key.
    """
    return Asymmetric.generate_key()


def test_generate_key(key_pair: tuple[rsa.RSAPublicKey, rsa.RSAPrivateKey]) -> None:
    """
    Test the key generation functionality of the Asymmetric class.

    Args:
        key_pair (tuple): A tuple containing the public and private RSA keys.

    Raises:
        AssertionError: If the public or private key is not of the expected type.
    """
    assert isinstance(
        key_pair[0], rsa.RSAPublicKey), "Public key must be an instance of rsa.RSAPublicKey"
    assert isinstance(
        key_pair[1], rsa.RSAPrivateKey), "Private key must be an instance of rsa.RSAPrivateKey"


@patch("algoritms.serialization.Serialization.deserialize_symmetric_key")
@patch("algoritms.serialization.Serialization.deserialize_public_key")
@patch("algoritms.serialization.Serialization.serialize_symmetric_key")
@patch("algoritms.functional.Functional.write_file_bytes")
def test_encrypt(
    mock_write: MagicMock,
    mock_serialize_symmetric: MagicMock,
    mock_deserialize_public: MagicMock,
    mock_deserialize_symmetric: MagicMock,
    key_pair: tuple[rsa.RSAPublicKey, rsa.RSAPrivateKey],
) -> None:
    """
    Test the encryption functionality of the Asymmetric class.

    Args:
        mock_write (MagicMock): Mock for writing encrypted data.
        mock_serialize_symmetric (MagicMock): Mock for serializing the symmetric key.
        mock_deserialize_public (MagicMock): Mock for deserializing the public key.
        mock_deserialize_symmetric (MagicMock): Mock for deserializing the symmetric key.
        key_pair (tuple): A tuple containing the RSA public and private keys.

    Raises:
        AssertionError: If the decrypted symmetric key doesn't match the original key.
    """
    symmetric_key: bytes = b";sU8maXF35_4hOki"
    public_key, private_key = key_pair

    mock_deserialize_symmetric.return_value = symmetric_key
    mock_deserialize_public.return_value = public_key

    Asymmetric.encrypt(
        "path/to/public", "path/to/symmetric_origin", "path/to/encrypted")

    mock_write.assert_called_once()
    encrypted_key: bytes = mock_write.call_args[0][1]

    mock_serialize_symmetric.return_value = None

    decrypted_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    assert decrypted_key == symmetric_key, "Decrypted key does not match the original symmetric key"


@patch("algoritms.serialization.Serialization.deserialize_symmetric_key")
@patch("algoritms.serialization.Serialization.deserialize_private_key")
@patch("algoritms.serialization.Serialization.serialize_symmetric_key")
def test_decrypt(
    mock_serialize_symmetric: MagicMock,
    mock_deserialize_private: MagicMock,
    mock_deserialize_symmetric: MagicMock,
    key_pair: tuple[rsa.RSAPublicKey, rsa.RSAPrivateKey],
) -> None:
    """
    Test the decryption functionality of the Asymmetric class.

    Args:
        mock_serialize_symmetric (MagicMock): Mock for serializing the symmetric key.
        mock_deserialize_private (MagicMock): Mock for deserializing the private key.
        mock_deserialize_symmetric (MagicMock): Mock for deserializing the encrypted symmetric key.
        key_pair (tuple): A tuple containing the RSA public and private keys.

    Raises:
        AssertionError: If the decrypted symmetric key doesn't match the original key.
    """
    symmetric_key: bytes = b";sU8maXF35_4hOki"
    public_key, private_key = key_pair

    encrypted_key = public_key.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    mock_deserialize_private.return_value = private_key
    mock_deserialize_symmetric.return_value = encrypted_key

    mock_serialize_symmetric.return_value = None

    decrypted_key = Asymmetric.decrypt(
        "path/to/private", "path/to/encrypted", "path/to/decrypted")

    mock_serialize_symmetric.assert_called_once()

    assert decrypted_key == symmetric_key, "Decrypted key does not match the original symmetric key"
