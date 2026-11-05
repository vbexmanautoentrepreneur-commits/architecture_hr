from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Employee:
    nom: str
    age: int
    service: str
    salary: float
    date_embauche: date
    email: str
    manager: str
    telephone: str
    ville: str
    pays: str
    date_naissance: date
    id: Optional[int] = None

    @property
    def anciennete_jours(self) -> int:
        return (date.today() - self.date_embauche).days

    @property
    def anciennete_annees(self) -> float:
        return round(self.anciennete_jours / 365.25, 2)

    @property
    def age_reel(self) -> int:
        today = date.today()

        return (
            today.year
            - self.date_naissance.year
            - ((today.month, today.day) < (self.date_naissance.month, self.date_naissance.day))
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nom": self.nom,
            "age": self.age,
            "service": self.service,
            "salary": self.salary,
            "date_embauche":  self.date_embauche.isoformat() if self.date_embauche else None,
            "email": self.email,
            "manager": self.manager,
            "telephone": self.telephone,
            "ville": self.ville,
            "pays": self.pays,
            "date_naissance": self.date_naissance.isoformat() if self.date_naissance else None
        }