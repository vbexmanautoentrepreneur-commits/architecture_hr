from pathlib import Path
from models.employee import Employee
from datetime import datetime
import pandas as pd

class EmployeeService:

    def __init__(self, csv_file):
        self.csv_file = Path(csv_file)
        if not self.csv_file.exists():
            df = pd.DataFrame(columns=["id", "nom", "age", "service", "salary",
                                       "date_embauche", "email","manager",
                                       "telephone","ville","pays","date_naissance"])
            df.to_csv(self.csv_file, index=False)

    def load_employees(self) -> list[Employee]:
        df = self.load()
        employees = []
        for _, row in df.iterrows():
            employees.append(
                Employee(
                    id=int(row["id"]),
                    nom=row["nom"],
                    age=int(row["age"]),
                    service=row["service"],
                    salary=float(row["salary"]),
                    date_embauche=datetime.strptime(row["date_embauche"], "%Y-%m-%d").date(),
                    email=row["email"],
                    manager=row["manager"],
                    telephone=row["telephone"],
                    ville=row["ville"],
                    pays=row["pays"],
                    date_naissance=datetime.strptime(row["date_naissance"], "%Y-%m-%d").date()
                )
            )
        return employees

    def load(self):
        return pd.read_csv(self.csv_file)

    def save(self, df):
        df.to_csv(self.csv_file, index=False)

    def list_employees(self):
        return self.load()

    def age_moyen(self):
        df = self.load()
        return df["age"].mean()

    def new_id(self):
        df = self.load()
        return df["id"].max()

    def add_employee(self, nom, age, service, salary,date_embauche,email,manager,telephone,ville,pays,date_naissance):
        if age < 18: raise ValueError("Le salarié doit avoir au moins 18 ans")
        if salary < 1000: raise ValueError("Le salaire doit superieur au smic")
        if "@" not in email: raise ValueError("Email invalide")
        if date_embauche > date_embauche.today(): raise ValueError("Date d'embauche future interdite")

        df = self.load()
        new_id = 1 if df.empty else int(df["id"].max()) + 1
        new_row = {"id": new_id, "nom": nom, "age": age, "service": service, "salary": salary,
                   "date_embauche": date_embauche, "email": email, "manager": manager,
                   "telephone":telephone,"ville":ville,"pays":pays,"date_naissance":date_naissance}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        self.save(df)
        return new_id

    def update_employee(self, employee_id, nom, age, service, salary,
                        date_embauche,email,manager,telephone,ville,pays,date_naissance):
        df = self.load()
        mask = df["id"] == employee_id
        if not mask.any(): return False
        df.loc[mask, "nom"] = nom
        df.loc[mask, "age"] = age
        df.loc[mask, "service"] = service
        df.loc[mask, "salary"] = salary
        df.loc[mask, "date_embauche"] = date_embauche
        df.loc[mask, "email"] = email
        df.loc[mask, "manager"] = manager
        df.loc[mask, "telephone"] = telephone
        df.loc[mask, "ville"] = ville
        df.loc[mask, "pays"] = pays
        df.loc[mask, "date_naissance"] = date_naissance
        self.save(df)
        return True

    def delete_employee(self, employee_id):
        df = self.load()
        before = len(df)
        df = df[df["id"] != employee_id]
        self.save(df)
        return len(df) < before

    def find_employee(self, employee_id):
        df = self.load()
        result = df[df["id"] == employee_id]
        if result.empty: return None
        return result.iloc[0]

