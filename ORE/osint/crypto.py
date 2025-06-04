import gnupg
from pathlib import Path

GPG_HOME = Path(__file__).resolve().parent / "gpg_home"
GPG_HOME.mkdir(exist_ok=True)

gpg = gnupg.GPG(gnupghome=str(GPG_HOME))


def generate_key(name: str, email: str, passphrase: str) -> str:
    """Generate a new PGP key and return the fingerprint."""
    input_data = gpg.gen_key_input(
        name_real=name,
        name_email=email,
        passphrase=passphrase,
    )
    key = gpg.gen_key(input_data)
    return key.fingerprint


def encrypt_text(text: str, recipient: str) -> str:
    """Encrypt text to the recipient."""
    encrypted = gpg.encrypt(text, recipients=[recipient])
    if not encrypted.ok:
        raise RuntimeError(encrypted.status)
    return str(encrypted)


def decrypt_text(text: str, passphrase: str) -> str:
    """Decrypt text using private key and passphrase."""
    decrypted = gpg.decrypt(text, passphrase=passphrase)
    if not decrypted.ok:
        raise RuntimeError(decrypted.status)
    return str(decrypted)


def encrypt_file(path: str, recipient: str, output: str) -> Path:
    """Encrypt a file for the recipient."""
    result = gpg.encrypt_file(
        file=open(path, "rb"),
        recipients=[recipient],
        output=output,
    )
    if not result.ok:
        raise RuntimeError(result.status)
    return Path(output)


def decrypt_file(path: str, passphrase: str, output: str) -> Path:
    """Decrypt an encrypted file."""
    result = gpg.decrypt_file(
        file=open(path, "rb"),
        passphrase=passphrase,
        output=output,
    )
    if not result.ok:
        raise RuntimeError(result.status)
    return Path(output)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="PGP Helper")
    sub = parser.add_subparsers(dest="cmd")

    gk = sub.add_parser("gen-key")
    gk.add_argument("name")
    gk.add_argument("email")
    gk.add_argument("passphrase")

    enc = sub.add_parser("encrypt")
    enc.add_argument("recipient")
    enc.add_argument("text")

    dec = sub.add_parser("decrypt")
    dec.add_argument("passphrase")
    dec.add_argument("text")

    args = parser.parse_args()
    if args.cmd == "gen-key":
        fp = generate_key(args.name, args.email, args.passphrase)
        print("Generated key:", fp)
    elif args.cmd == "encrypt":
        print(encrypt_text(args.text, args.recipient))
    elif args.cmd == "decrypt":
        print(decrypt_text(args.text, args.passphrase))
    else:
        parser.print_help()
