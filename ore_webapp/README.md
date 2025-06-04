# Operation Rising Ember Web Application

This directory contains a basic scaffold for a secure, locally hostable web application for Operation Rising Ember (ORE). The application uses FastAPI for the backend and basic HTML/JavaScript for the frontend.

## Features

- **User Authentication** with hashed passwords and token-based session management.
- **Encrypted File Storage** using symmetric encryption (Fernet).
- **Dashboard** visualizing mission data with map overlays and time series charts. Charts can be exported to images or PDFs.
- **Modular Apps** so new functionality can be added easily.

All data is stored locally in SQLite and encrypted files remain offline. The app can be extended to integrate optional APIs for mapping or OSINT if needed.

Run `uvicorn backend.main:app --reload` from this directory to start the server.
