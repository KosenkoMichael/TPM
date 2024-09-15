import sys
import argparse

sys.path.append("algoritms")

from constants import GYBRID_SYSTEM_SYMMETRIC_KEY_SIZE
from algoritms.asymmetric_cipher import Asymmetric
from algoritms.symmetric_cipher import Symmetric
from algoritms.serialization import Serialization
from algoritms.functional import Functional


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "mode",
        type = str,
        help = "key_generation OR encryption OR decryption",
    )
    args = parser.parse_args()

    settings = Functional.read_json("settings.json")

    def generate_gibrid_system_keys():
        # Symmetric key generation and serialization
        symmetric_key = Symmetric.generate_key( GYBRID_SYSTEM_SYMMETRIC_KEY_SIZE )
        Serialization.serialize_symmetric_key(
            settings["symmetric_key"],
            symmetric_key
        )

        # Asymmetric key generation and serialization
        public_key, private_key = Asymmetric.generate_key()
        Serialization.serialize_public_key( settings["public_key"], public_key )
        Serialization.serialize_private_key( settings["private_key"], private_key )

        print("keys was generated")

    def encrypt_gibrid_sistem():
        # Text encryption
        encrypted_text = Symmetric.encrypt(
            settings["initial_file"],
            settings["symmetric_key"],
            settings["nonce"],
            settings["encrypted_file"],
        )
        # Symmetric key encryption
        Asymmetric.encrypt(
            settings["public_key"],
            settings["symmetric_key"],
            settings["encrypted_symmetric_key"],
        )

        print("text was encrypted")

    def decrypt_gibrid_sistem():
        # Symmetric key decryption
        Asymmetric.decrypt(
            settings["private_key"],
            settings["encrypted_symmetric_key"],
            settings["decrypted_symmetric_key"],
        )

        # Text decryption
        decrypted_text = Symmetric.decrypt(
            settings["symmetric_key"],
            settings["nonce"],
            settings["encrypted_file"],
            settings["decrypted_file"],
        )
        print(f"Decrypted text: {decrypted_text}")

    task = {
        "key_generation" : generate_gibrid_system_keys,
        "encryption"     : encrypt_gibrid_sistem,
        "decryption"     : decrypt_gibrid_sistem,
    }
    task[f"{args.mode}"]()


if __name__ == "__main__":
    main()
