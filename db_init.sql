CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER,
                gender TEXT,
                id_number TEXT,
                description TEXT,
                additional_information TEXT
            );

CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER,
                time TEXT,
                ai_diagnosis TEXT,
                final_diagnosis TEXT,
                doctor_note TEXT,
                FOREIGN KEY (patient_id) REFERENCES patients(id)
            );

-- INSERT INTO history (patient_id, time, ai_diagnosis, final_diagnosis) VALUES
-- (1, '2024-04-30 08:00:00', 'AI diagnosis for patient 1 - 1', 'Final diagnosis for patient 1 - 1'),
-- (1, '2024-04-30 09:00:00', 'AI diagnosis for patient 1 - 2', 'Final diagnosis for patient 1 - 2'),
-- (2, '2024-04-30 10:00:00', 'AI diagnosis for patient 2 - 1', 'Final diagnosis for patient 2 - 1'),
-- (2, '2024-04-30 11:00:00', 'AI diagnosis for patient 2 - 2', 'Final diagnosis for patient 2 - 2'),
-- (3, '2024-04-30 12:00:00', 'AI diagnosis for patient 3 - 1', 'Final diagnosis for patient 3 - 1'),
-- (3, '2024-04-30 13:00:00', 'AI diagnosis for patient 3 - 2', 'Final diagnosis for patient 3 - 2'),
-- (4, '2024-04-30 14:00:00', 'AI diagnosis for patient 4 - 1', 'Final diagnosis for patient 4 - 1'),
-- (4, '2024-04-30 15:00:00', 'AI diagnosis for patient 4 - 2', 'Final diagnosis for patient 4 - 2'),
-- (5, '2024-04-30 16:00:00', 'AI diagnosis for patient 5 - 1', 'Final diagnosis for patient 5 - 1'),
-- (5, '2024-04-30 17:00:00', 'AI diagnosis for patient 5 - 2', 'Final diagnosis for patient 5 - 2'),
-- (6, '2024-04-30 18:00:00', 'AI diagnosis for patient 6 - 1', 'Final diagnosis for patient 6 - 1'),
-- (6, '2024-04-30 19:00:00', 'AI diagnosis for patient 6 - 2', 'Final diagnosis for patient 6 - 2'),
-- (7, '2024-04-30 20:00:00', 'AI diagnosis for patient 7 - 1', 'Final diagnosis for patient 7 - 1'),
-- (7, '2024-04-30 21:00:00', 'AI diagnosis for patient 7 - 2', 'Final diagnosis for patient 7 - 2'),
-- (8, '2024-04-30 22:00:00', 'AI diagnosis for patient 8 - 1', 'Final diagnosis for patient 8 - 1'),
-- (8, '2024-04-30 23:00:00', 'AI diagnosis for patient 8 - 2', 'Final diagnosis for patient 8 - 2'),
-- (9, '2024-05-01 00:00:00', 'AI diagnosis for patient 9 - 1', 'Final diagnosis for patient 9 - 1'),
-- (9, '2024-05-01 01:00:00', 'AI diagnosis for patient 9 - 2', 'Final diagnosis for patient 9 - 2'),
-- (10, '2024-05-01 02:00:00', 'AI diagnosis for patient 10 - 1', 'Final diagnosis for patient 10 - 1'),
-- (10, '2024-05-01 03:00:00', 'AI diagnosis for patient 10 - 2', 'Final diagnosis for patient 10 - 2');


-- INSERT INTO patients (name, age, gender, id_number, description, additional_information) VALUES
-- ('Aliceeee', 30, 'Female', '1234567890', 'Description of Alice', 'Additional diagnosis for Alice');

