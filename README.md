# Database Setup

## 1. Prerequisites
- PostgreSQL installed
- `psql` available in terminal

---

## 2. Create the Database

Open terminal and run:

psql -U postgres

Inside `psql`:

CREATE DATABASE orkuflaediisland;
\q

---

## 3. Run the SQL File

Navigate to the folder containing `DDL_DML.sql`:

cd DATABASE/Legacy_schema

Run:

psql -U postgres -d orkuflaediisland -f DDL_DML.sql

---

## 4. Verify Setup

Open `psql` again:

psql -U postgres

Then run:

\c orkuflaediisland  
\dt raforka_legacy.*

Check that data exists:

SELECT COUNT(*) FROM raforka_legacy.orku_maelingar;

---

## 5. (Optional) Set Default Schema

ALTER DATABASE orkuflaediisland SET search_path TO raforka_legacy, public;

---

## Notes

- Tables are created in schema: `raforka_legacy`
- Errors about missing role (e.g. `bjarki1312`) can be ignored