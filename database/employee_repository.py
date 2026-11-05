from database.db import get_connection
from models.employee import Employee
from datetime import date

class EmployeeRepository:

    def get_by_id(self, employee_id):
        conn = get_connection()
        row = conn.execute("SELECT * FROM employees WHERE id=?", (employee_id,)).fetchone()
        conn.close()
        if not row:
            return None
        return Employee(
            id=row["id"],
            nom=row["nom"],
            age=row["age"],
            service=row["service"],
            salary=row["salary"],
            date_embauche=date.fromisoformat(row["date_embauche"]),
            email=row["email"],
            manager=row["manager"],
            telephone=row["telephone"],
            ville=row["ville"],
            pays=row["pays"],
            date_naissance=date.fromisoformat(row["date_naissance"])
        )

    def get_all(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(""" SELECT * FROM Employees ORDER BY nom """)
        rows = cursor.fetchall()
        conn.close()
        return rows

    def add(self, Employee):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                        INSERT INTO Employees( nom, age, service, salary, date_embauche,
                         email, manager, telephone, ville, pays, date_naissance ) VALUES( ?,?,?,?,?,?,?,?,?,?,? ) """,
                        (Employee.nom, Employee.age, Employee.service, Employee.salary, Employee.date_embauche.isoformat(),
                         Employee.email, Employee.manager, Employee.telephone, Employee.ville, Employee.pays, Employee.date_naissance.isoformat()))
        conn.commit()
        conn.close()

    def update(self, Employee):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(""" UPDATE Employees SET nom=?, age=?, service=?, salary=?, date_embauche=?,
                         email=?, manager=?, telephone=?, ville=?, pays=?, date_naissance=? WHERE id=?
                        """,(Employee.nom, Employee.age, Employee.service, Employee.salary, Employee.date_embauche.isoformat(),
                            Employee.email, Employee.manager, Employee.telephone, Employee.ville,
                             Employee.pays, Employee.date_naissance.isoformat(), Employee.id))
        conn.commit()
        conn.close()

    def delete(self, Employee_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(""" DELETE FROM Employees WHERE id=? """, (Employee_id,))
        conn.commit()
        conn.close()

    def search(self, text):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(""" SELECT * FROM Employees WHERE nom LIKE ? OR service LIKE ? OR manager LIKE ? """,
                       (f"%{text}%", f"%{text}%", f"%{text}%"))
        result = cursor.fetchall()
        conn.close()
        return result

    def get_kpis(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(""" SELECT COUNT(*) as effectif, AVG(age) as age_moyen,
         AVG(salary) as salaire_moyen, SUM(salary) as masse FROM Employees """)
        result = cursor.fetchone()
        conn.close()
        return result

    def add_history(self, user, Employee_id, field, old_value, new_value):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(""" INSERT INTO history( modification_date, user_name, Employee_id, field_name, old_value, new_value )
                        VALUES( datetime('now'), ?, ?, ?, ?, ? ) """,
                       (user, Employee_id, field, str(old_value), str(new_value)))
        conn.commit()
        conn.close()