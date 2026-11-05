from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QPushButton, QHBoxLayout, QMessageBox, QComboBox, QVBoxLayout, QGroupBox
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QIcon
from datetime import date

class AddEmployeeDialog(QDialog):

    def __init__(self, employee=None):
        super().__init__()
        self.employee = employee
        self.setWindowTitle("Modifier un employé" if employee else "Ajouter un employé")
        self.setWindowIcon(QIcon("icons/app.png"))
        self.resize(600, 650)
        self.build_ui()
        if employee:
            self.load_employee()

    def build_ui(self):

        self.setStyleSheet("""
        QDialog { background-color: #f5f6fa; }
        QGroupBox { background-color: white; border: 1px solid #dcdde1; border-radius: 10px; margin-top: 10px; font-weight: bold; padding-top: 15px; }
        QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }
        QLineEdit,
        QSpinBox { background: white; border: 1px solid #dcdde1; border-radius: 6px; padding-left: 5px; min-height: 30px; }
        QSpinBox::up-button { width: 20px; }
        QSpinBox::down-button { width: 20px; }
        QDoubleSpinBox {  background: white;border: 1px solid #dcdde1; border-radius: 6px; padding-left: 6px; min-height: 28px; },
        QDoubleSpinBox::up-button { width: 20px; }
        QDoubleSpinBox::down-button { width: 20px; }
        QDateEdit,
        QComboBox { background: white; border: 1px solid #dcdde1; border-radius: 6px; padding: 6px; min-height: 28px; }
        QLineEdit:focus,
        QSpinBox:focus,
        QDoubleSpinBox:focus,
        QDateEdit:focus,
        QComboBox:focus { border: 2px solid #3498db; }
        QPushButton { background-color: #3498db; color: white; border: none; border-radius: 8px; padding: 10px; font-weight: bold; min-width: 120px; }
        QPushButton:hover { background-color: #2980b9; }
        """)

        main_layout = QVBoxLayout()

        rh_group = QGroupBox("Informations RH")
        rh_layout = QFormLayout()

        self.nom = QLineEdit()
        self.nom.setPlaceholderText("Nom complet")

        self.service = QComboBox()
        self.service.addItems(["IT", "QA", "RH", "Management", "Finance"])

        self.manager = QLineEdit()

        self.salary = QSpinBox()
        self.salary.setMaximum(999999)
        self.salary.setSingleStep(10)
        self.salary.setSuffix(" €")

        self.date_embauche = QDateEdit()
        self.date_embauche.setCalendarPopup(True)
        self.date_embauche.setDate(QDate.currentDate())

        rh_layout.addRow("Nom", self.nom)
        rh_layout.addRow("Service", self.service)
        rh_layout.addRow("Manager", self.manager)
        rh_layout.addRow("Salaire", self.salary)
        rh_layout.addRow("Date embauche", self.date_embauche)
        rh_group.setLayout(rh_layout)
        rh_group.setStyleSheet(""" QGroupBox { background-color: #E3F2FD; border: 2px solid #2196F3; 
                                               border-radius: 10px; font-weight: bold; margin-top: 10px; padding-top: 15px; } """)
        contact_group = QGroupBox("Coordonnées")
        contact_group.setStyleSheet(""" QGroupBox { background-color: #E8F5E9; border: 2px solid #4CAF50; 
                                               border-radius: 10px; font-weight: bold; margin-top: 10px; padding-top: 15px; } """)
        contact_layout = QFormLayout()
        self.email = QLineEdit()
        self.email.setPlaceholderText("prenom.nom@entreprise.com")
        self.telephone = QLineEdit()
        self.telephone.setPlaceholderText("0612345678")
        self.ville = QLineEdit()
        self.pays = QComboBox()
        self.pays.addItems(["France", "Belgique", "Espagne", "Allemagne", "Italie"])
        contact_layout.addRow("Email", self.email)
        contact_layout.addRow("Téléphone", self.telephone)
        contact_layout.addRow("Ville", self.ville)
        contact_layout.addRow("Pays", self.pays)
        contact_group.setLayout(contact_layout)
        perso_group = QGroupBox("Informations personnelles")
        perso_layout = QFormLayout()
        perso_group.setStyleSheet(""" QGroupBox { background-color: #FFF3E0; border: 2px solid #FF9800; 
                                                  border-radius: 10px; font-weight: bold; margin-top: 10px; padding-top: 15px; } """)
        self.age = QSpinBox()
        self.age.setRange(18, 100)
        self.age.setAccelerated(True)

        self.date_naissance = QDateEdit()
        self.date_naissance.setCalendarPopup(True)
        self.date_naissance.setDate(QDate.currentDate())
        self.date_naissance.dateChanged.connect(self.calculate_age)

        perso_layout.addRow("Âge", self.age)
        perso_layout.addRow("Date de naissance", self.date_naissance)
        perso_group.setLayout(perso_layout)
        stats_group = QGroupBox("Statistiques")
        stats_layout = QFormLayout()
        self.anciennete = QLineEdit()
        self.anciennete.setReadOnly(True)
        self.age_reel = QLineEdit()
        self.age_reel.setReadOnly(True)
        stats_layout.addRow("Age calculé", self.age_reel)
        stats_layout.addRow("Ancienneté", self.anciennete)
        stats_group.setLayout(stats_layout)
        stats_group.setStyleSheet(""" QGroupBox { background-color: #F3E5F5; border: 2px solid #9C27B0; 
                                                   border-radius: 10px; font-weight: bold; margin-top: 10px; padding-top: 15px; } """)

        self.btn_ok = QPushButton("Enregistrer" if self.employee else "Ajouter")
        self.btn_cancel = QPushButton("Annuler")

        self.btn_ok.clicked.connect(self.validate)
        self.btn_ok.setStyleSheet("""
                                        QPushButton { background-color: #27AE60; color: white; border: none; border-radius: 8px; padding: 10px;
                                                        min-width: 140px; min-height: 40px; font-size: 12pt; font-weight: bold; }
                                        QPushButton:hover { background-color: #229954; }
                                        QPushButton:pressed { background-color: #1E8449; }
                                        """)
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_cancel.setStyleSheet("""
                                        QPushButton { background-color: #E74C3C; color: white; border: none; border-radius: 8px; padding: 10px;
                                                        min-width: 140px; min-height: 40px; font-size: 12pt; font-weight: bold; }
                                        QPushButton:hover { background-color: #CB4335; }
                                        QPushButton:pressed { background-color: #B03A2E; }
                                        """)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.btn_ok)
        button_layout.addWidget(self.btn_cancel)

        main_layout.addWidget(rh_group)
        main_layout.addWidget(contact_group)
        main_layout.addWidget(perso_group)
        main_layout.addWidget(stats_group)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.calculate_age()
        self.calculate_seniority()

    def load_employee(self):

        self.nom.setText(self.employee.nom)
        self.age.setValue(self.employee.age)
        self.service.setCurrentText(self.employee.service)
        self.salary.setValue(self.employee.salary)
        self.email.setText(self.employee.email)
        self.manager.setText(self.employee.manager)
        self.telephone.setText(str(self.employee.telephone))
        self.ville.setText(self.employee.ville)
        self.pays.setCurrentText(self.employee.pays)

        if self.employee.date_embauche:
            self.date_embauche.setDate(QDate(self.employee.date_embauche.year, self.employee.date_embauche.month, self.employee.date_embauche.day))

        if self.employee.date_naissance:
            self.date_naissance.setDate(QDate(self.employee.date_naissance.year, self.employee.date_naissance.month, self.employee.date_naissance.day))

        self.calculate_age()
        self.calculate_seniority()



    def calculate_age(self):

        naissance = self.date_naissance.date().toPyDate()
        today = date.today()
        age = (today.year - naissance.year - ((today.month, today.day) < (naissance.month, naissance.day)))
        self.age_reel.setText(f"your age is {age}")

    def calculate_seniority(self):
        embauche = self.date_embauche.date().toPyDate()
        today = date.today()
        years = today.year - embauche.year
        months = today.month - embauche.month
        days = today.day - embauche.day
        if days < 0:
            months -= 1
            days += 30
        if months < 0:
            years -= 1
            months += 12
        self.anciennete.setText(f"{years} an(s) {months} mois")

    def validate(self):

        if not self.nom.text().strip():
            QMessageBox.warning(self, "Erreur", "Le nom est obligatoire")
            return

        if not self.email.text().strip():
            QMessageBox.warning(self, "Erreur", "L'email est obligatoire")
            return

        if "@" not in self.email.text():
            QMessageBox.warning(self, "Erreur", "Email invalide")
            return

        self.accept()

    def get_data(self):

        return {
            "nom": self.nom.text(),
            "age": self.age.value(),
            "service": self.service.currentText(),
            "salary": self.salary.value(),
            "date_embauche": self.date_embauche.date().toPyDate(),
            "email": self.email.text(),
            "manager": self.manager.text(),
            "telephone": self.telephone.text(),
            "ville": self.ville.text(),
            "pays": self.pays.currentText(),
            "date_naissance": self.date_naissance.date().toPyDate()
        }