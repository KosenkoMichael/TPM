import sys
import argparse

sys.path.append("algoritms")


from algoritms.asymmetric_cipher import Asymmetric
from algoritms.symmetric_cipher import Symmetric
from algoritms.serialization import Serialization
from algoritms.functional import Functional


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "mode", type=str, help="key_generation OR encryption OR decryption"
    )
    args = parser.parse_args()

    settings = Functional.read_json("settings.json")

    def gibrid_system_keys_generation():
        # Symmetric key generation and serialization
        symmetric_key = Symmetric.key_generation(32)
        Serialization.symmetric_key_serialization(
            settings["symmetric_key"], symmetric_key
        )

        # Asymmetric key generation and serialization
        public_key, private_key = Asymmetric.key_generation()
        Serialization.public_key_serialization(settings["public_key"], public_key)
        Serialization.private_key_serialization(settings["private_key"], private_key)

        print("keys was generated")

    def gibrid_sistem_encryption():
        # Text encryption
        encrypted_text = Symmetric.encryption(
            settings["initial_file"],
            settings["symmetric_key"],
            settings["nonce"],
            settings["encrypted_file"],
        )
        # Symmetric key encryption
        Asymmetric.encryption(
            settings["public_key"],
            settings["symmetric_key"],
            settings["encrypted_symmetric_key"],
        )

        print("text was encrypted")

    def gibrid_sistem_decryption():
        # Symmetric key decryption
        Asymmetric.decryption(
            settings["private_key"],
            settings["encrypted_symmetric_key"],
            settings["decrypted_symmetric_key"],
        )

        # Text decryption
        decrypted_text = Symmetric.decryption(
            settings["symmetric_key"],
            settings["nonce"],
            settings["encrypted_file"],
            settings["decrypted_file"],
        )
        print(f"Decrypted text: {decrypted_text}")

    task = {
        "key_generation": gibrid_system_keys_generation,
        "encryption": gibrid_sistem_encryption,
        "decryption": gibrid_sistem_decryption,
    }
    task[f"{args.mode}"]()


if __name__ == "__main__":
    main()
