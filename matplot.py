import matplotlib.pyplot as plt
from services.employee_service import EmployeeService

myclass=EmployeeService(r'data/employees.csv')
employees = myclass.load_employees()

employees_sorted = sorted(
    employees,
    key=lambda e: e.salary,
    reverse=True
)

noms = [e.nom for e in employees_sorted]
salaires = [e.salary for e in employees_sorted]

plt.figure(figsize=(8, 4))
plt.bar(noms, salaires, color="steelblue")

plt.title("Salaires par employé")
plt.ylabel("Salaire (€)")

plt.tight_layout()
plt.show()
