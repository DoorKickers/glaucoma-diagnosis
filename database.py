import sqlite3

class Database:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def get_patients(self):
        self.cursor.execute("SELECT * FROM Patients")
        rows = self.cursor.fetchall()
        patients = []
        for row in rows:
            patient = dict(row)
            self.cursor.execute("SELECT COUNT(*) FROM history WHERE patient_id = ?", (patient['id'],))
            count = self.cursor.fetchone()[0]
            patient['diaged'] = bool(count > 0)
            patients.append(patient)
        return patients

    def get_historys(self, patient_id):
        self.cursor.execute('SELECT * FROM history WHERE patient_id = ?', (patient_id,))
        rows = self.cursor.fetchall()
        historys = []
        for row in rows:
            history = dict(row)
            historys.append(history)
        return historys

    def update_patient(self, patient_id, name, age, gender, id_number, description, additional_information):
            result = self.cursor.execute('''
                UPDATE patients 
                SET name=?, age=?, gender=?, id_number=?, description=?, additional_information=?
                WHERE id=?
            ''', (name, age, gender, id_number, description, additional_information, patient_id))
            self.conn.commit()
    
    def add_history(self, patient_id, time, ai_diag, final_diag, doctor_note):
        self.cursor.execute('''
            INSERT INTO history (patient_id, time, ai_diagnosis, final_diagnosis, doctor_note)
            VALUES (?, ?, ?, ?, ?)
        ''', (patient_id, time, ai_diag, final_diag, doctor_note))
        self.conn.commit()

    def update_history(self, history_id, time, ai_diag, final_diag, doctor_note):
        self.cursor.execute('''
            UPDATE history 
            SET time=?, ai_diagnosis=?, final_diagnosis=?, doctor_note=?
            WHERE id=?
        ''', (time, ai_diag, final_diag, doctor_note, history_id))
        self.conn.commit()


if __name__ == "__main__":
    db = Database("/home/naitnal/Code/DL/remember_download_first_try/v0/demo.db")
    patients = db.get_patients()

    # 调用方式
    print(patients[0]["name"])  # 获取第一个人的名字
    print(patients[0]["diaged"])
