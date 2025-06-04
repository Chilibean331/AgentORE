# Trusted Contacts Directory

This repository now includes a simple command line tool for managing a confidential directory of trusted contacts and allies.  The directory stores:

- Name and organization
- Phone or email details
- Trust rating
- Tags for country, city, mission role, or threat level
- Encrypted relationship notes
- Activity log entries
- Linked documents such as signed MOUs

When you run the tool, it creates a `contacts_data` directory if it does not already exist.
All data is stored in `contacts_data/contacts.json` and any attached documents are copied into `contacts_data/documents/`.

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
# AgentORE Platform

This repository contains resources for Operation Rising Ember, including prompts, reports, and an OSINT toolkit.

## OSINT Toolkit

The `ORE/osint` module provides basic automation for scraping news, monitoring social media, collecting satellite imagery metadata, and storing intelligence. The toolkit supports exporting results to CSV and PDF, and generates an interactive map of collected incidents.
Use the generated `osint_map.html` to view collected intel on an interactive map.

See `ORE/osint/README.md` for details.


## Mission Task Board

The web application now includes endpoints and a simple UI for managing mission
tasks. Tasks can be created with fields for mission phase, urgency, location and
the responsible user. Status updates and assignments allow the app to act as a
basic Kanban board. Visit `tasks.html` after starting the server to add or view
tasks.

Daily or weekly status reports can be retrieved at `/tasks/reports/daily` or
`/tasks/reports/weekly`.


The `ore_webapp` directory provides a local FastAPI web application. It now includes an interactive dashboard with map overlays and time series charts summarizing mission data. Charts can be exported directly from the browser.

- The OSINT module now includes PGP utilities (`ORE/osint/crypto.py`) for
  encrypting notes or files with OpenPGP.


