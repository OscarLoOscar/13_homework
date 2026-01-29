## Django API Data Sync Project

This project facilitates automated data synchronization from the DummyJSON API (including Users, Products, and Carts) and integrates a comprehensive Django Management Command suite to handle the Data Lifecycle (CRUD).

---

## Table of Contents

- [Standard Development Commands](#standard-development-commands)
- [Core Logic and Implementation](#core-logic-and-implementation-crud--sync)
- [Frontend Data Visualization](#frontend-data-visualization)
- [Environment Configuration](#environment-configuration-env)

---

### Standard Development Commands

You can execute `./setup_data.sh` to initialize the project automatically, or manually run the following `python manage.py` commands:

#### 1. Database Initialization (Migrations)

Whenever modifications are made to `models.py`, these steps must be executed:

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 2. Data Synchronization Commands (Custom Fetch Data)

The `fetch_data` command supports various action parameters for flexible data management:

| Command                                       | Action         | Description                                                                |
| --------------------------------------------- | -------------- | -------------------------------------------------------------------------- |
| `python manage.py fetch_data`                 | Sync (Default) | Deletes existing data and fetches 25 fresh records from the API.           |
| `python manage.py fetch_data --action update` | Update         | Updates prices and ratings for existing products without deleting records. |
| `python manage.py fetch_data --action delete` | Delete         | Wipes all associated User, Product, and Cart records from the database.    |

#### 3. Start Development Server

```bash
python manage.py runserver
```

##### Automation Script:

First :

```bash
chmod +x setup_data.sh
```

Second :

```bash
./setup_data.sh
```

This script streamlines the initialization process:

1. Applies database migrations.
2. Executes `fetch_data` (Create/Sync).
3. Launches the `runserver` command.

#### Frontend Data Visualization

- Dashboard: Access http://localhost:8000/dashboard/ to view synchronized data across three distinct tables.

- Interactive Features:
  - ##### Product Description:
    Utilizes Bootstrap Collapse components (Open/Close buttons) to optimize screen space and readability.
  - ##### User-Cart Linking:
    Data is structurally linked, allowing for future expansion such as displaying purchase histories per user.

---

### Environment Configuration (.env)

#### Remember to add .env to your .gitignore file

## <span style="color:red; font-size:30px; font-weight:bold;">Remember!Remember!Remember!</span>

To keep sensitive information secure and out of the version control system (Git), this project uses a `.env` file. This file stores configuration variables that Django reads during runtime.

#### Before setup `.env` need to have `python 3.x and PostgreSQL or your using DB`

#### How to Set Up the .env File

1. In the root directory of the project (the same folder as manage.py), create a new file named .env.

2. Open the file and add the following variables:

```Plaintext
DEBUG=True
SECRET_KEY=your-custom-secret-key-here
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=127.0.0.1
DB_PORT=5432
```

---

#### Generate a secure `SECRET_KEY` in Django

It's best to use a string that is `at least 50 characters` long and contains `a mix of letters, numbers, and symbols` in string .

Here is a freshly generated, secure `SECRET_KEY` for your .env file:

```Plaintext
django-insecure-m#*p&_v8v8(l!k-x8_u-t5^h%0+h_@j!7q9z(tq*y#9)7(1-7_
```

#### How to Apply This

1. Open your .env file.

2. Replace your-custom-secret-key-here with the string above.

3. Ensure there are no spaces around the `=` sign: `SECRET_KEY=django-insecure-m#*p&_v8v8(l!k-x8_u-t5^h%0+h_@j!7q9z(tq*y#9)7(1-7_`# 13_homework
