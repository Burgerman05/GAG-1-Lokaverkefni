-- Task C3

CREATE TYPE station_type_enum AS ENUM (
    'power_plant',
    'substation'
);


-- Orku_einingar table (Energy units)
CREATE TABLE orku_einingar (
    id SERIAL PRIMARY KEY,
    heiti VARCHAR(100) NOT NULL,  -- Name
    tegund_stod station_type_enum,  -- Station type
    x_hnit NUMERIC(10, 6),  -- X coordinate
    y_hnit NUMERIC(10, 6),  -- Y coordinate
    uppsetning DATE  -- Installation date
);

-- Tegund_mælingar table (Measurement types)
CREATE TABLE tegund_mælingar (
    id SERIAL PRIMARY KEY,
    tegund VARCHAR(50) NOT NULL,  -- Type
    lysing TEXT  -- Description
);

-- Notandi table (Customers/Users)
CREATE TABLE notandi (
    id SERIAL PRIMARY KEY,
    notandi_heiti VARCHAR(100) NOT NULL UNIQUE  -- Customer name
);

-- Stod table (Stations)
CREATE TABLE stod (
    id SERIAL PRIMARY KEY,
    heiti VARCHAR(100) NOT NULL,  -- Name
    x_hnit NUMERIC(10, 6),  -- X coordinate
    y_hnit NUMERIC(10, 6),  -- Y coordinate
    tegnd_stod VARCHAR(50),  -- Station type description
    uppsetning DATE  -- Installation date
);

-- Mælingar table (Measurements) - Connects to Orku_einingar
CREATE TABLE mælingar (
    id SERIAL PRIMARY KEY,
    orku_eining_id INTEGER NOT NULL REFERENCES orku_einingar(id),
    tegund_mælingar_id INTEGER NOT NULL REFERENCES tegund_mælingar(id),
    notandi_id INTEGER REFERENCES notandi(id),  -- Optional, for customer measurements
    gildi_kwh NUMERIC(15, 6) NOT NULL,  -- Value in kWh
    timi TIMESTAMP NOT NULL,  -- Time of measurement
    sendandi_mælingar VARCHAR(100),  -- Sender of measurement
    has_measurement BOOLEAN DEFAULT TRUE
);

-- Station keeps track of orku_einingar (1:1)
CREATE TABLE stod_orku_track (
    stod_id INTEGER PRIMARY KEY REFERENCES stod(id),
    orku_eining_id INTEGER UNIQUE NOT NULL REFERENCES orku_einingar(id),
    track_since DATE DEFAULT CURRENT_DATE
);

-- Power plants inject substations (N:1)
CREATE TABLE power_plant_injection (
    id SERIAL PRIMARY KEY,
    power_plant_id INTEGER NOT NULL REFERENCES orku_einingar(id),
    substation_id INTEGER NOT NULL REFERENCES stod(id),
    inject_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    loss_percentage NUMERIC(5, 2)  -- Optional loss tracking
);

-- Customer withdraws energy from substations (1:N)
CREATE TABLE customer_withdrawal (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES notandi(id),
    substation_id INTEGER NOT NULL REFERENCES stod(id),
    withdraw_m NUMERIC(15, 6),  -- Withdrawal amount
    withdrawal_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



-- Mesurments has Measurement type (1:N) - Additional mapping table
CREATE TABLE measurements_type_mapping (
    id SERIAL PRIMARY KEY,
    measurement_id INTEGER NOT NULL REFERENCES mælingar(id),
    measurement_type_id INTEGER NOT NULL REFERENCES tegund_mælingar(id),
    measure_value NUMERIC(15, 6),
    measure_timestamp TIMESTAMP
);

-- indexes

CREATE INDEX idx_mælingar_orku_eining ON mælingar(orku_eining_id);
CREATE INDEX idx_mælingar_tegund ON mælingar(tegund_mælingar_id);
CREATE INDEX idx_mælingar_notandi ON mælingar(notandi_id);
CREATE INDEX idx_mælingar_timi ON mælingar(timi);
CREATE INDEX idx_stod_heiti ON stod(heiti);
CREATE INDEX idx_orku_einingar_heiti ON orku_einingar(heiti);
CREATE INDEX idx_notandi_heiti ON notandi(notandi_heiti);
CREATE INDEX idx_power_plant_injection_plant ON power_plant_injection(power_plant_id);
CREATE INDEX idx_customer_withdrawal_customer ON customer_withdrawal(customer_id);

-- Insert measurement types
INSERT INTO tegund_mælingar (tegund, lysing) VALUES
    ('Framleiðsla', 'Production measurement'),
    ('Innmötun', 'Injection measurement'),
    ('Úttekt', 'Withdrawal measurement');
-- Task D1
