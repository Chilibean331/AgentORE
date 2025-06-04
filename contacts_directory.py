import argparse
import json
import os
import sys
import hashlib
import base64
from datetime import datetime
from typing import List, Dict

DATA_DIR = os.path.join(os.path.dirname(__file__), "contacts_data")
DB_FILE = os.path.join(DATA_DIR, "contacts.json")
DOCS_DIR = os.path.join(DATA_DIR, "documents")


def ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(DOCS_DIR, exist_ok=True)


def load_db() -> Dict[str, List[Dict]]:
    if not os.path.exists(DB_FILE):
        return {"contacts": []}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_db(db: Dict[str, List[Dict]]):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)


def derive_key(password: str) -> bytes:
    return hashlib.sha256(password.encode("utf-8")).digest()


def xor_encrypt(text: str, password: str) -> str:
    key = derive_key(password)
    data = text.encode("utf-8")
    encrypted = bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])
    return base64.b64encode(encrypted).decode("utf-8")


def xor_decrypt(token: str, password: str) -> str:
    key = derive_key(password)
    data = base64.b64decode(token)
    decrypted = bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])
    return decrypted.decode("utf-8")


def next_id(db: Dict[str, List[Dict]]) -> int:
    if not db["contacts"]:
        return 1
    return max(c["id"] for c in db["contacts"]) + 1


def add_contact(args):
    db = load_db()
    cid = next_id(db)
    note_enc = xor_encrypt(args.note or "", args.password)
    contact = {
        "id": cid,
        "name": args.name,
        "organization": args.org,
        "phone": args.phone,
        "email": args.email,
        "trust_rating": args.trust,
        "tags": args.tags.split(",") if args.tags else [],
        "notes_encrypted": note_enc,
        "activity_log": [],
        "documents": [],
    }
    db["contacts"].append(contact)
    save_db(db)
    print(f"Added contact {cid}: {args.name}")


def list_contacts(args):
    db = load_db()
    for c in db["contacts"]:
        print(f"{c['id']}: {c['name']} ({c['organization']})")


def search_contacts(args):
    db = load_db()
    results = []
    for c in db["contacts"]:
        if args.name and args.name.lower() not in c["name"].lower():
            continue
        if args.tag:
            if not any(args.tag.lower() in t.lower() for t in c.get("tags", [])):
                continue
        results.append(c)
    for c in results:
        print(f"{c['id']}: {c['name']} - tags: {', '.join(c.get('tags', []))}")


def view_contact(args):
    db = load_db()
    contact = next((c for c in db["contacts"] if c["id"] == args.id), None)
    if not contact:
        print("Contact not found")
        return
    print(json.dumps({k: v for k, v in contact.items() if k != "notes_encrypted"}, indent=2))
    if args.password:
        try:
            note = xor_decrypt(contact["notes_encrypted"], args.password)
            print("Notes:\n" + note)
        except Exception:
            print("Failed to decrypt notes. Wrong password?")


def add_log(args):
    db = load_db()
    contact = next((c for c in db["contacts"] if c["id"] == args.id), None)
    if not contact:
        print("Contact not found")
        return
    entry = {
        "date": datetime.utcnow().isoformat() + "Z",
        "entry": args.entry,
    }
    contact.setdefault("activity_log", []).append(entry)
    save_db(db)
    print("Log entry added")


def attach_document(args):
    db = load_db()
    contact = next((c for c in db["contacts"] if c["id"] == args.id), None)
    if not contact:
        print("Contact not found")
        return
    if not os.path.exists(args.file):
        print("File does not exist")
        return
    basename = os.path.basename(args.file)
    dest = os.path.join(DOCS_DIR, f"{contact['id']}_{basename}")
    with open(args.file, "rb") as src, open(dest, "wb") as dst:
        dst.write(src.read())
    contact.setdefault("documents", []).append(dest)
    save_db(db)
    print(f"Document {basename} attached to contact {contact['id']}")


def main():
    ensure_dirs()
    parser = argparse.ArgumentParser(description="Trusted contacts directory")
    sub = parser.add_subparsers(dest="command")

    add = sub.add_parser("add", help="Add a contact")
    add.add_argument("--name", required=True)
    add.add_argument("--org", default="")
    add.add_argument("--phone", default="")
    add.add_argument("--email", default="")
    add.add_argument("--trust", type=int, default=0)
    add.add_argument("--tags", default="")
    add.add_argument("--note", default="")
    add.add_argument("--password", required=True)
    add.set_defaults(func=add_contact)

    sub_list = sub.add_parser("list", help="List contacts")
    sub_list.set_defaults(func=list_contacts)

    search = sub.add_parser("search", help="Search contacts")
    search.add_argument("--name")
    search.add_argument("--tag")
    search.set_defaults(func=search_contacts)

    view = sub.add_parser("view", help="View contact")
    view.add_argument("--id", type=int, required=True)
    view.add_argument("--password")
    view.set_defaults(func=view_contact)

    log = sub.add_parser("log", help="Add activity log entry")
    log.add_argument("--id", type=int, required=True)
    log.add_argument("--entry", required=True)
    log.set_defaults(func=add_log)

    attach = sub.add_parser("attach", help="Attach document")
    attach.add_argument("--id", type=int, required=True)
    attach.add_argument("--file", required=True)
    attach.set_defaults(func=attach_document)

    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        sys.exit(1)
    args.func(args)


if __name__ == "__main__":
    main()
