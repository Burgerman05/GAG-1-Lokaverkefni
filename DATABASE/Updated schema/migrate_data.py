from datetime import date

import polars as pl
import psycopg2


def get_db_connection() -> psycopg2.connection:
    conn = psycopg2.connect(
        dbname="final_project",
        user="postgres",
        password="Admin123",
        host="localhost",
        port=5432,
    )
    conn.set_client_encoding("UTF8")
    return conn


def migrate_entities() -> None:
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 1. Load Legacy Data into Polars
        df_legacy_users = pl.read_database(
            "SELECT * FROM raforka_legacy.notendur_skraning", conn
        )
        df_legacy_units = pl.read_database(
            "SELECT * FROM raforka_legacy.orku_einingar", conn
        )

        # 2. Migrate Owners (eigandi)
        all_owners = (
            pl.concat(
                [df_legacy_users.select("eigandi"), df_legacy_units.select("eigandi")]
            )
            .unique()
            .drop_nulls()
        )

        for row in all_owners.iter_rows():
            cursor.execute(
                "INSERT INTO raforka_updated.eigandi (heiti) VALUES (%s) ON CONFLICT DO NOTHING",
                (row[0],),
            )

        # Fetch new owner mapping
        df_owners_map = pl.read_database(
            "SELECT id AS eigandi_id, heiti AS eigandi FROM raforka_updated.eigandi",
            conn,
        )

        # 3. Migrate Stations (stod)
        df_stod = df_legacy_units.join(df_owners_map, on="eigandi", how="left")

        # Create dates and handle nulls
        stod_data = df_stod.select(
            [
                pl.col("heiti"),
                pl.col("tegund_stod"),
                pl.col("eigandi_id"),
                pl.struct(["ar_uppsett", "manudir_uppsett", "dagur_uppsett"])
                .map_elements(
                    lambda s: date(
                        s["ar_uppsett"],
                        s["manudir_uppsett"] or 1,
                        s["dagur_uppsett"] or 1,
                    ),
                    return_dtype=pl.Date,
                )
                .alias("uppsetning"),
                pl.col("X_HNIT").alias("x_hnit"),
                pl.col("Y_HNIT").alias("y_hnit"),
            ]
        )

        for row in stod_data.iter_rows():
            cursor.execute(
                """INSERT INTO raforka_updated.stod (heiti, tegund_stod, eigandi_id, uppsetning, x_hnit, y_hnit)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                row,
            )

        # 4. Specialized Stations (power_plant / substation)
        df_stod_map = pl.read_database(
            "SELECT id, heiti FROM raforka_updated.stod", conn
        )
        df_specialized = df_legacy_units.select(["heiti", "tegund"]).join(
            df_stod_map, on="heiti"
        )

        for row in df_specialized.filter(pl.col("tegund") == "virkjun").iter_rows():
            cursor.execute(
                "INSERT INTO raforka_updated.power_plant (id) VALUES (%s)", (row[2],)
            )

        for row in df_specialized.filter(pl.col("tegund") == "stod").iter_rows():
            cursor.execute(
                "INSERT INTO raforka_updated.substation (id) VALUES (%s)", (row[2],)
            )

        # 5. Self-referencing IDs (tengd_stod_ID)
        df_links = df_legacy_units.select(["heiti", "tengd_stod"]).drop_nulls()
        df_links = df_links.join(df_stod_map, on="heiti").join(
            df_stod_map.rename({"id": "parent_id", "heiti": "tengd_stod"}),
            on="tengd_stod",
        )

        for row in df_links.iter_rows():
            cursor.execute(
                "UPDATE raforka_updated.stod SET tengd_stod_id = %s WHERE id = %s",
                (row[3], row[2]),
            )

        # 6. Migrate Users (notendur_skraning)
        df_users = df_legacy_users.join(df_owners_map, on="eigandi", how="left").select(
            ["heiti", "kennitala", "eigandi_id", "ar_stofnad", "X_HNIT", "Y_HNIT"]
        )

        for row in df_users.iter_rows():
            cursor.execute(
                """INSERT INTO raforka_updated.notendur_skraning (heiti, kennitala, eigandi_id, ar_stofnad, x_hnit, y_hnit)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                row,
            )

        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error during entity migration: {e}")
    finally:
        cursor.close()
        conn.close()


def migrate_measurements_from_legacy_db() -> None:
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query_legacy = "SELECT * FROM raforka_legacy.orku_maelingar"
        df_measurements = pl.read_database(query_legacy, conn)

        df_stod = pl.read_database(
            "SELECT id as plant_id, heiti as eining_heiti FROM raforka_updated.stod",
            conn,
        )
        df_subs = pl.read_database(
            "SELECT id as sub_id, heiti as sendandi_maelingar FROM raforka_updated.stod",
            conn,
        )
        df_owners = pl.read_database(
            "SELECT id as owner_id, heiti as sendandi_maelingar FROM raforka_updated.eigandi",
            conn,
        )
        df_users = pl.read_database(
            "SELECT id as user_id, heiti as notandi_heiti FROM raforka_updated.eigandi",
            conn,
        )

        df_enriched = df_measurements.join(df_stod, on="eining_heiti", how="left")
        df_enriched = df_enriched.join(df_users, on="notandi_heiti", how="left")

        for row in df_enriched.iter_rows(named=True):
            m_type = row["tegund_maelingar"].strip() if row["tegund_maelingar"] else ""
            cursor.execute(
                """INSERT INTO raforka_updated.maelingar (power_plant_ID, gildi_kwh, timi, maeling_type)
                   VALUES (%s, %s, %s, %s) RETURNING id""",
                (row["plant_id"], row["gildi_kwh"], row["timi"], m_type),
            )
            new_measurement_id = cursor.fetchone()[0]

            if m_type == "Úttekt":
                sender_matches = df_subs.filter(
                    pl.col("sendandi_maelingar") == row["sendandi_maelingar"]
                )
                if not sender_matches.is_empty():
                    sendandi_id = sender_matches.select("sub_id").item()
                    cursor.execute(
                        "INSERT INTO raforka_updated.uttekt (id, sendandi_maelingar, notandi_id) VALUES (%s, %s, %s)",
                        (new_measurement_id, sendandi_id, row["user_id"]),
                    )

            elif m_type == "Innmötun":
                sender_matches = df_subs.filter(
                    pl.col("sendandi_maelingar") == row["sendandi_maelingar"]
                )
                if not sender_matches.is_empty():
                    sendandi_id = sender_matches.select("sub_id").item()
                    cursor.execute(
                        "INSERT INTO raforka_updated.innmotun (id, sendandi_maelingar) VALUES (%s, %s)",
                        (new_measurement_id, sendandi_id),
                    )

            elif m_type == "Framleiðsla":
                sender_matches = df_owners.filter(
                    pl.col("sendandi_maelingar") == row["sendandi_maelingar"]
                )
                if not sender_matches.is_empty():
                    owner_id = sender_matches.select("owner_id").item()
                    cursor.execute(
                        "INSERT INTO raforka_updated.framleidsla (id, sendandi_maelingar) VALUES (%s, %s)",
                        (new_measurement_id, owner_id),
                    )

        conn.commit()
        print("Measurement migration completed successfully.")

    except Exception as e:
        conn.rollback()
        print(f"Migration failed: {e}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    migrate_entities()
    migrate_measurements_from_legacy_db()