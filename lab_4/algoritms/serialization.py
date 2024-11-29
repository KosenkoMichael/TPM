"""
This module implements the functionality of serialization and deserialization of encryption keys
"""
import logging


from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
    load_pem_private_key,
)
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


logger = logging.getLogger("info_logger")
error_logger = logging.getLogger("error_logger")


class Serialization:
    """
    This class contains the definition of functions for serializing
    and deserializing symmetric and asymmetric encryption keys
    """
    def __init__( self ):
        logger.info("serialization class initialize")

    def serialize_symmetric_key(
            file_path : str,
            key       : bytes
        ) -> None:
        """Serialization of the symmetric encryption key
        Args:
            file_path : file_path for serialization
            key       : symmetric key
        """
        try:
            with open( file_path, "wb" ) as key_file:
                logger.info(f"serialization to {file_path}")
                key_file.write(key)
            
        except Exception as error:
            error_logger.error(f"{error}")

    def deserialize_symmetric_key( file_path: str ) -> bytes:
        """Deserialization of the symmetric encryption key
        Args:
            file_path: file_path for deserialization
        Returns:
            symmetric key
        """
        try:
            with open( file_path, "rb" ) as key_file:
                logger.info(f"deserialization from {file_path}")
                return key_file.read()
            
        except Exception as error:
            error_logger.error(f"{error}")

    def serialize_public_key(
            public_pem : str,
            public_key : rsa.RSAPublicKey
        ) -> None:
        """RSA public key serialization
        Args:
            public_pem : file_path for public RSA key serialization
            public_key : public RSA-key
        """
        try:
            with open( public_pem, "wb" ) as public_out:
                logger.info(f"serialization to {public_pem}")
                public_out.write(
                    public_key.public_bytes(
                        encoding = serialization.Encoding.PEM,
                        format = serialization.PublicFormat.SubjectPublicKeyInfo,
                    )
                )
            
        except Exception as error:
            error_logger.error(f"{error}")

    def serialize_private_key(
        private_pem : str,
        private_key : rsa.RSAPrivateKey
    ) -> None:
        """RSA private key serialization
        Args:
            private_pem : file_path for private RSA key serialization
            private_key : private RSA-key
        """
        try:
            with open( private_pem, "wb" ) as private_out:
                logger.info(f"serialization to {private_pem}")
                private_out.write(
                    private_key.private_bytes(
                        encoding = serialization.Encoding.PEM,
                        format = serialization.PrivateFormat.TraditionalOpenSSL,
                        encryption_algorithm = serialization.NoEncryption(),
                    )
                )
            
        except Exception as error:
            error_logger.error(f"{error}")

    def deserialize_public_key( public_pem: str ) -> rsa.RSAPublicKey:
        """RSA public key deserialization
        Args:
            public_pem: file_path for public RSA key deserialization
        Returns:
            RSA public Key
        """
        try:
            with open( public_pem, "rb" ) as pem_in:
                logger.info(f"deserialization from {public_pem}")
                public_bytes = pem_in.read()
            
            return load_pem_public_key( public_bytes )
        except Exception as error:
            error_logger.error(f"{error}")

    def deserialize_private_key( private_pem: str ) -> rsa.RSAPrivateKey:
        """RSA private key deserialization
        Args:
            private_pem: file_path for private RSA key deserialization
        Returns:
            RSA private Key
        """
        try:
            with open( private_pem, "rb" ) as pem_in:
                logger.info(f"deserialization from {private_pem}")
                private_bytes = pem_in.read()
            
            return load_pem_private_key(
                private_bytes,
                password = None,
            )
        except Exception as error:
            error_logger.error(f"{error}")
 