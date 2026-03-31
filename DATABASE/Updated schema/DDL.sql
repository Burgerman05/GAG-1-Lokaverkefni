-- Task C3
DROP SCHEMA IF EXISTS raforka_updated CASCADE;

SET client_encoding = 'UTF8';

CREATE SCHEMA raforka_updated;

CREATE TABLE raforka_updated.eigandi (
    ID SERIAL PRIMARY KEY,
    heiti VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE raforka_updated.stod (
    ID SERIAL PRIMARY KEY,
    heiti VARCHAR(100) NOT NULL,
    tegund_stod VARCHAR(100) NOT NULL,
    eigandi_ID INTEGER NOT NULL REFERENCES raforka_updated.eigandi(ID) NOT NULL,
    uppsetning DATE NOT NULL,

    x_hnit DOUBLE PRECISION NOT NULL,
    y_hnit DOUBLE PRECISION NOT NULL,

    tengd_stod_ID INTEGER REFERENCES raforka_updated.stod(ID),
    CONSTRAINT check_unique_ids CHECK (ID <> tengd_stod_ID)
);

CREATE TABLE raforka_updated.power_plant (
    ID INTEGER PRIMARY KEY REFERENCES raforka_updated.stod(ID)
);

CREATE TABLE raforka_updated.substation (
    ID INTEGER PRIMARY KEY REFERENCES raforka_updated.stod(ID)
);

CREATE TABLE raforka_updated.notendur_skraning (
    ID SERIAL PRIMARY KEY,
    heiti VARCHAR(100) NOT NULL UNIQUE,
    kennitala VARCHAR(10) NOT NULL UNIQUE,
    eigandi_ID INTEGER NOT NULL REFERENCES raforka_updated.eigandi(ID) NOT NULL,
    ar_stofnad INTEGER NOT NULL,

    x_hnit DOUBLE PRECISION NOT NULL,
    y_hnit DOUBLE PRECISION NOT NULL
);

CREATE TABLE raforka_updated.maelingar (
    ID SERIAL PRIMARY KEY,
    power_plant_ID INTEGER REFERENCES raforka_updated.power_plant(ID) NOT NULL,
    gildi_kwh NUMERIC NOT NULL,
    timi TIMESTAMP without time zone NOT NULL,
    maeling_type VARCHAR(50) NOT NULL
);

CREATE TABLE raforka_updated.uttekt (
    ID SERIAL PRIMARY KEY REFERENCES raforka_updated.maelingar(ID),
    sendandi_maelingar INTEGER REFERENCES raforka_updated.substation(ID) NOT NULL,
    notandi_id INTEGER REFERENCES raforka_updated.eigandi(ID) NOT NULL
);
CREATE TABLE raforka_updated.innmotun (
    ID SERIAL PRIMARY KEY REFERENCES raforka_updated.maelingar(ID),
    sendandi_maelingar INTEGER REFERENCES raforka_updated.substation(ID) NOT NULL
);
CREATE TABLE raforka_updated.framleidsla (
    ID SERIAL PRIMARY KEY REFERENCES raforka_updated.maelingar(ID),
    sendandi_maelingar INTEGER REFERENCES raforka_updated.eigandi(ID) NOT NULL
);

CREATE OR REPLACE VIEW raforka_updated.allar_maelingar AS
SELECT
    PP.heiti,
    M.timi,
    M.gildi_kwh,
    M.maeling_type
FROM raforka_updated.maelingar M
LEFT JOIN raforka_updated.stod PP ON M.power_plant_ID = PP.ID;

CREATE TABLE raforka_updated.test_measurement (
    id integer NOT NULL,
    timi timestamp without time zone,
    value numeric
);

-- Task D1

-- Indexes
CREATE INDEX idx_maelingar ON raforka_updated.maelingar (timi, power_plant_ID);
