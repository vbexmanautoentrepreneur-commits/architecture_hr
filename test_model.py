from services.employee_service import EmployeeService
from dataclasses import fields

myclass=EmployeeService(r'data/employees.csv')
employees = myclass.load_employees()

for employee in employees:
    print("-" * 30)
    for field in fields(employee):
        print(f"{field.name:<15}: {getattr(employee, field.name)}")


result = {}
for emp in employees:
    result.setdefault(emp.manager, 0)
    result[emp.manager] += emp.salary


print(result)
age_moyen = myclass.age_moyen()
print(f"Âge moyen : {age_moyen:.1f} ans")


print(f"{'ID':<5} {'Nom':<15} {'Service':<10} {'Salaire':>10}")
print("-" * 45)

for employee in employees:
    print(
        f"{employee.id:<5} "
        f"{employee.nom:<15} "
        f"{employee.service:<10} "
        f"{employee.salary:>10.2f}"
    )

for employee in sorted(employees, key=lambda e: e.salary, reverse=True):
    print(
        f"{employee.nom:<15} "
        f"{employee.salary:>10.2f} €"
    )

total = sum(emp.salary for emp in employees)
moyenne = total / len(employees)

print(f"Masse salariale : {total:.2f} €")
print(f"Salaire moyen   : {moyenne:.2f} €")