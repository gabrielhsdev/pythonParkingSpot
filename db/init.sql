CREATE TABLE floors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    level INT NOT NULL UNIQUE,  -- Ensure level is unique and required
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE parking_spots (
    id INT AUTO_INCREMENT PRIMARY KEY,
    floor_id INT NOT NULL,  -- Foreign key referencing the floors table
    spot_number VARCHAR(50) NOT NULL,  -- Spot number/identifier for the parking spot
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (floor_id) REFERENCES floors(id) ON DELETE CASCADE,
    CONSTRAINT unique_spot_per_floor UNIQUE (floor_id, spot_number)  -- Ensure unique spot number per floor
);


CREATE TABLE cars (
    id INT AUTO_INCREMENT PRIMARY KEY,
    license_plate VARCHAR(255) NOT NULL,  -- Unique license plate for identification
    parking_spot_id INT NOT NULL,  -- Foreign key referencing the parking spots table
    arrive_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Time when the car entered the parking spot
    leave_at TIMESTAMP,  -- Time when the car leaves (NULL if not left yet)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parking_spot_id) REFERENCES parking_spots(id) ON DELETE CASCADE,
    CONSTRAINT unique_license_plate_per_spot UNIQUE (parking_spot_id, license_plate, leave_at)
);

-- Insert 3 floors into the floors table
INSERT INTO floors (name, level) VALUES 
    ('Floor 1', 1),
    ('Floor 2', 2),
    ('Floor 3', 3);

-- Insert 5 parking spots for each floor into the parking_spots table
-- For Floor 1
INSERT INTO parking_spots (floor_id, spot_number) VALUES
    (1, 'A1'),
    (1, 'A2'),
    (1, 'A3'),
    (1, 'A4'),
    (1, 'A5');

-- For Floor 2
INSERT INTO parking_spots (floor_id, spot_number) VALUES
    (2, 'B1'),
    (2, 'B2'),
    (2, 'B3'),
    (2, 'B4'),
    (2, 'B5');

-- For Floor 3
INSERT INTO parking_spots (floor_id, spot_number) VALUES
    (3, 'C1'),
    (3, 'C2'),
    (3, 'C3'),
    (3, 'C4'),
    (3, 'C5');