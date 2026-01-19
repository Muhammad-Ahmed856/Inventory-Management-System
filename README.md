# Inventory Management System

Simple command-line inventory management tool written in Python.

## Overview

This repository contains an interactive terminal application that demonstrates a small role-based inventory system. It stores inventory and user data as JSON files and is intended as a starter project or learning example.

## Files

- `inventory.py` — main application.
- `users.json` — example data


## Prerequisites

- Python 3.8 or newer.

## Installation

1. (Optional) Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate    # Windows
```

2. Install dependencies (none required by default):

```bash
pip install -r requirements.txt
```

## Usage

1. If you have a `users.json` file, keep it in the project root. Otherwise copy the example:

```bash
copy users.json    # Windows
```

2. Run the application:

```bash
python inventory.py
```

The app creates default data files when they are missing.

## users.json

The `users.json` file provides template user accounts (admin/manager/staff). 

## Requirements

This project uses only the Python standard library by default. If you add third-party packages, pin them in `requirements.txt`.

## License

This project is licensed under the MIT License — see the `LICENSE` file.


