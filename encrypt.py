import subprocess
import sys


def encrypt_file(password, input_file, output_file):
    """Encrypt any file in the salted AES format CryptoJS can decrypt."""
    subprocess.run(
        [
            "openssl",
            "enc",
            "-aes-256-cbc",
            "-salt",
            "-md",
            "md5",
            "-a",
            "-A",
            "-in",
            input_file,
            "-out",
            output_file,
            "-pass",
            f"pass:{password}",
        ],
        check=True,
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python encrypt.py <password> [input_file] [output_file]")
        sys.exit(1)

    password = sys.argv[1]
    input_file = sys.argv[2] if len(sys.argv) > 2 else "plain.txt"
    output_file = sys.argv[3] if len(sys.argv) > 3 else "encrypted.txt"

    try:
        encrypt_file(password, input_file, output_file)
    except (FileNotFoundError, subprocess.CalledProcessError) as error:
        print(f"❌ Encryption failed: {error}")
        sys.exit(1)

    print(f"💌 Encrypted successfully → {output_file}")
