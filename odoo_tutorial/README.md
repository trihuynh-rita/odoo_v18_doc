# Odoo Tutorial & Documentation

## Installation & Setup

### Clone Odoo v19 Source
To download Odoo v19 from the official repository, run:
```bash
git clone https://github.com/odoo/odoo.git --branch 19.0 --depth 1 odoo_src_v19
```
*Note: Use `--depth 1` to speed up the download by fetching only the latest commit.*

## Odoo Setup & Running

After the database is started, you can run Odoo using the following commands.

### 1. Initialize Virtual Environment
Ensure your virtual environment is active:
```bash
source .venv/bin/activate
```

### 2. Run Odoo for the first time (Initialization)
If you are using a new database (e.g., `cinema_db`), run:
```bash
python odoo_src/odoo-bin -c odoo.conf -d cinema_db -i base,cinema_management
```

### 3. Run Odoo for Development (with Auto-reload)
Use `--dev=all` to automatically restart the server when Python files are changed.
```bash
python odoo_src/odoo-bin -c odoo.conf -u cinema_management --dev=all
```

### 4. Basic Run Command
```bash
python odoo_src/odoo-bin -c odoo.conf
```

## Useful Docker Commands

**Access PostgreSQL directly:**
```bash
docker exec -it postgres-db psql -U odoo -d cinema_db
```

**View database health:**
```bash
docker-compose ps
```


## 5. Setting up PyCharm Run Configuration

To easily run or debug Odoo directly using the **Run/Debug** button in PyCharm without typing terminal commands, follow these steps:

1. Click on the **Run Configuration** dropdown at the top right of PyCharm (usually says "Current File" or "Add Configuration...").
2. Click **Edit Configurations...**
3. Click the **+** (Add New Configuration) button at the top left and select **Python**.
4. Configure the following fields:
   - **Name:** `Odoo Dev` (or any name you prefer)
   - **Script path:** Open the folder icon and select the `odoo-bin` file (located in `odoo_src/odoo-bin`).
   - **Parameters:** `-c odoo.conf -u cinema_management --dev=all`
   - **Python interpreter:** Select the Python interpreter of your virtual environment (`.venv/bin/python`).
   - **Working directory:** Make sure this points to your root project folder (e.g., `25_03_2025`).
5. Click **Apply** and then **OK**.

Now, you can just click the Green Play button (Run) or Bug button (Debug) to easily start Odoo.
