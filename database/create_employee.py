from datetime import date
from models.employee import Employee
from database.employee_repository import EmployeeRepository
employee = Employee(
    nom="Karine",
    age=39,
    service="RH",
    salary=5000.0,
    date_embauche=date(2023, 5, 15),
    email="karine@gmail.com",
    manager="Titi",
    telephone="0666666666",
    ville="Caen",
    pays="France",
    date_naissance=date(1987, 2, 14)
)
print(employee.anciennete_annees)
print(employee.to_dict())
EmployeeRepository().add(employee)