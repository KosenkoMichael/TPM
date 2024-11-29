"""
This module implements functionality (key generation, encryption and decryption) 
for symmetric encryption
"""
import os
import logging

from cryptography.hazmat.primitives.ciphers import(
    Cipher,
    algorithms,
)
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

from constants import(
    NONCE_SYMMETRIC_KEY_SIZE,
    PKCS7_BLOCK_SIZE,
)
from serialization import Serialization
from functional import Functional

logger = logging.getLogger("symmetric_cipher")


class Symmetric:
    """
    This class provides the definition of key generation functions for
    symmetric encryption, as well as encryption and decryption using it
    """
    def __init__(self):
        logger.info("symmetric_cipher class initialize")

    def generate_key( bytes_num: int ) -> bytes:
        """generate symmetric key

        Args:
            bytes_num (int):key_len

        Returns:
            bytes: symmetric key
        """
        logger.info(f"symmetric key was generated len = {bytes_num} bytes")
        return os.urandom(bytes_num)

    def encrypt(
        text_file_path           : str,
        path_to_symmetric        : str,
        path_to_nonce            : str,
        encrypted_text_file_path : str,
    ) -> bytes:
        """encryption by symmetric key

        Args:
            text_file_path (str)           : path to origin text
            path_to_symmetric (str)        : path to symmetric key
            path_to_nonce (str)            : path to nonce for ChaCha20
            encrypted_text_file_path (str) : file path for encrypted text

        Returns:
            str: encrypted text
        """
        # Generate nonse
        nonce = Symmetric.generate_key( NONCE_SYMMETRIC_KEY_SIZE )
        Serialization.serialize_symmetric_key( path_to_nonce, nonce )
        origin_text = Functional.read_file( text_file_path )
        symmetric_key = Serialization.deserialize_symmetric_key( path_to_symmetric )
        cipher = Cipher(
            algorithms.ChaCha20( symmetric_key, nonce ),
            None,
            backend = default_backend()
        )
        # Text padding
        padder = padding.PKCS7( PKCS7_BLOCK_SIZE ).padder()
        text_to_bytes = bytes( origin_text, "UTF-8" )
        padded_text = padder.update( text_to_bytes ) + padder.finalize()
        # Initialize encryptor
        encryptor = cipher.encryptor()
        # Text encryption
        encrypted_text = encryptor.update( padded_text ) + encryptor.finalize()
        Functional.write_file_bytes( encrypted_text_file_path, encrypted_text )
        logger.info(f"encrypt from {text_file_path} to {encrypted_text_file_path}")
        return encrypted_text

    def decrypt(
        path_to_symmetric      : str,
        path_to_nonce          : str,
        path_to_encrypted_text : str,
        path_to_decrypted_text : str,
    ) -> str:
        """decryption by symmetric key

        Args:
            path_to_symmetric (str)      : path to key
            path_to_nonce (str)          : path to nonce for ChaCha20
            path_to_encrypted_text (str) : path to encrypted file
            path_to_decrypted_text (str) : path to decrypted file

        Returns:
            str: decrypted text
        """
        # Reading nonce
        nonce = Functional.read_file_bytes( path_to_nonce )
        encrypted_text = Functional.read_file_bytes( path_to_encrypted_text )
        symmetric_key = Serialization.deserialize_symmetric_key( path_to_symmetric )
        cipher = Cipher(
            algorithms.ChaCha20( symmetric_key, nonce ),
            mode = None,
            backend = default_backend(),
        )
        # Initialize decryptor
        decryptor = cipher.decryptor()
        # Text decryption
        decrypted_text = decryptor.update( encrypted_text ) + decryptor.finalize()
        # Text unpadding
        unpadder = padding.PKCS7( PKCS7_BLOCK_SIZE ).unpadder()
        unpadded_dc_text = unpadder.update( decrypted_text ) + unpadder.finalize()
        dec_unpad_text = unpadded_dc_text.decode("UTF-8")
        Functional.write_file( path_to_decrypted_text, dec_unpad_text )
        logger.info(f"decrypt from {path_to_encrypted_text} to {path_to_decrypted_text}")
        return dec_unpad_text
 