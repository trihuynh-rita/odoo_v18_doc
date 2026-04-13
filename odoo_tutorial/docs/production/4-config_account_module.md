---
name: 4-config_account_module.md
description: Comprehensive A-Z guide for configuring the Odoo Accounting module, localization, and OCA financial reports.
---

# Odoo Accounting Module Configuration: A-Z Guide

This document provides a complete guide to setting up and configuring the accounting environment in Odoo, integrating the Vietnam localization package, and installing the OCA Financial Reports.

## 1. Core Modules Overview

*   **`account` (Invoicing):** The core Odoo module used to manage customer invoices, vendor bills, and overall financial obligations.
*   **`l10n_vn` (Vietnam - Accounting):** The essential localization package that provides the standard chart of accounts according to Vietnamese accounting standards (Circular 200/2014/TT-BTC or 133/2016/TT-BTC), pre-configured VAT tax rates, and sets the default currency to VND.
*   **`account_financial_report` (OCA):** A core module from the Odoo Community Association (OCA) ecosystem. It unlocks full financial reporting features (General Ledger, Balance Sheet, P&L, etc.) normally restricted in the Community edition.

## 2. Phase 1: Source Code and Environment Preparation

There are two primary approaches to setting up the environment. Option 2 is highly recommended for macOS users to ensure a stable, isolated environment without Python or library conflicts.

### Option 1: Native Installation (Ubuntu/Linux)

#### 1.A. Clone Source Code
Create the project structure and download the required source code.

```bash
mkdir ~/odoo_erp_project
cd ~/odoo_erp_project

# Clone Odoo Community Core (Depth 1 for faster download)
git clone https://github.com/odoo/odoo.git -b 18.0 --depth 1 odoo_core

# Clone Custom Addons (OCA Financial Reports and Web Dependencies)
mkdir custom_addons
cd custom_addons
git clone https://github.com/OCA/account-financial-reporting.git -b 18.0
git clone https://github.com/OCA/web.git -b 18.0
cd ..
```

#### 1.B. Fix Font and PDF Rendering Issues
To ensure standard Vietnamese characters render correctly in exported PDF reports, install the appropriate fonts and the Qt-patched version of `wkhtmltopdf`.

```bash
# 1. Install Vietnamese MS Core Fonts
sudo apt-get update
sudo apt-get install -y ttf-mscorefonts-installer fontconfig
# Clear font cache
fc-cache -f -v

# 2. Install Qt-patched wkhtmltopdf (Ubuntu 22.04 example)
# Do NOT use 'apt install wkhtmltopdf' directly without the official package.
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb
sudo apt install -y ./wkhtmltox_0.12.6.1-2.jammy_amd64.deb
```

#### 1.C. Set Up Python Dependencies and Configuration
Use a virtual environment to manage Odoo dependencies.

```bash
sudo apt install -y python3-venv python3-pip
python3 -m venv odoo-venv
source odoo-venv/bin/activate

# Install Odoo requirements
pip3 install -r odoo_core/requirements.txt
```

Create an `odoo.conf` file in the root `odoo_erp_project` directory to specify database credentials and module paths:

```ini
[options]
admin_passwd = admin_super_password
db_host = localhost
db_port = 5432
db_user = odoo
db_password = your_db_password
# Include the core addons and the newly cloned OCA addons sequentially
addons_path = ./odoo_core/addons, ./custom_addons/account-financial-reporting, ./custom_addons/web
```

Start the Odoo server:

```bash
./odoo_core/odoo-bin -c odoo.conf
```
*Odoo will now be running at `http://localhost:8069`.*

### Option 2: Docker Compose Installation (Highly Recommended for Mac)

If you are developing on a Mac, using Docker is the perfect solution. It completely isolates Odoo, PostgreSQL, and `wkhtmltopdf` into separate containers, keeping your Mac clean and preventing Python library conflicts.

#### 2.A. Install Docker Desktop
Download and install Docker Desktop for Mac from the official Docker website.

#### 2.B. Create `docker-compose.yml`
In the `~/odoo_erp_project` directory, create a `docker-compose.yml` file and paste the following code:

```yaml
version: '3.1'
services:
  web:
    image: odoo:18.0
    depends_on:
      - db
    ports:
      - "8069:8069"
    volumes:
      - odoo-web-data:/var/lib/odoo
      - ./odoo.conf:/etc/odoo/odoo.conf
      - ./custom_addons:/mnt/extra-addons
    environment:
      - HOST=db
      - USER=odoo
      - PASSWORD=odoo_db_password

  db:
    image: bitnami/postgresql:15
    environment:
      - POSTGRESQL_USERNAME=odoo
      - POSTGRESQL_PASSWORD=odoo_db_password
      - POSTGRESQL_DATABASE=postgres
    volumes:
      - odoo-db-data:/bitnami/postgresql

volumes:
  odoo-web-data:
  odoo-db-data:
```

#### 2.C. Launch the System
Run the following single command in the Terminal (inside the directory containing the `yml` file):

```bash
docker compose up -d
```
*The system will automatically pull the secure Bitnami PostgreSQL image, the Odoo image (which includes a Linux-native `wkhtmltopdf`), and map your `custom_addons` directory containing the OCA code. Open your browser and access `http://localhost:8069`.*

## 3. Phase 2: UI Installation and Configuration (Strict Sequence)

To avoid constraint violations and database errors, you **must** install the modules via the Odoo interface in the exact sequence outlined below.

### Step 1: Create a New Database
1.  Access `http://localhost:8069`.
2.  Fill in the database creation form. **Important:** Select `Vietnam` as the Country to ensure the system recognizes the localization context by default.

### Step 2: Install the Core Invoicing Module
1.  Navigate to the **Apps** menu.
2.  Search for **Invoicing** (`account`) and click **Install**. This initializes foundational database tables.

### Step 3: Install the Vietnam Accounting Package
1.  Clear the "Apps" filter in the search bar.
2.  Search for **Vietnam - Accounting** (`l10n_vn`) and install it.
3.  **Configuration:** Go to *Settings -> Accounting -> Fiscal Localization*. Ensure the correct standard (e.g., Vietnamese Accounting System - Circular 200 or 133) is applied to your company.

### Step 4: Install the OCA Financial Reports
1.  Go to *Settings*, scroll to the bottom, and click **Activate the developer mode**.
2.  Return to the **Apps** menu, click **Update Apps List** in the top navigation bar, and confirm.
3.  Search for `account_financial_report` and click **Install**.

## 4. Phase 3: Utilizing the OCA Financial Reports

The OCA reporting suite emphasizes query performance, strict inheritance (`_inherit`), and standardization.

*   **Accessing Reports:** Navigate to *Invoicing/Accounting -> Reporting*. The extended accounting reports will be listed here.
*   **Professional Exports (PDF/Excel):**
    *   **Excel:** Generates immense datasets rapidly by fetching data exactly at the moment of export rather than pre-loading.
    *   **PDF:** Layouts are optimized following the standard Odoo QWeb engine. After configuring the correct fonts in Phase 1, the Vietnamese text will be perfectly formatted.
*   **Dynamic Drill-down Views:** Reports support hierarchical tree views. Accountants can smoothly drop down from grouped aggregate accounts to the individual Journal Entry level.