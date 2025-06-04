# Trusted Contacts Directory

This repository now includes a simple command line tool for managing a confidential directory of trusted contacts and allies.  The directory stores:

- Name and organization
- Phone or email details
- Trust rating
- Tags for country, city, mission role, or threat level
- Encrypted relationship notes
- Activity log entries
- Linked documents such as signed MOUs

The data is saved in `contacts_data/contacts.json` and any attached documents are copied into `contacts_data/documents/`.

## Encryption
Notes for each contact are symmetrically encrypted using a basic XOR method derived from the password you provide. While this obfuscates the notes, it is **not** a substitute for strong cryptography.

## Usage
Run the script with Python 3:

```bash
python3 contacts_directory.py add --name "John Doe" --org "Acme" \
    --phone "+1-555-1234" --email "john@example.com" \
    --trust 5 --tags "country:US,city:NYC,mission:intel" \
    --note "Met in 2022" --password "mysecret"
```

Other commands include:

- `list` – list all contacts
- `search` – search by `--name` or `--tag`
- `view` – show a contact's details and decrypt notes with `--password`
- `log` – add an activity log entry
- `attach` – attach a document to a contact

Example:

```bash
python3 contacts_directory.py log --id 1 --entry "Called to verify information"
```

```bash
python3 contacts_directory.py attach --id 1 --file /path/to/MOU.pdf
```

Ensure that the `contacts_data` directory is kept secure, as it contains all stored information.
