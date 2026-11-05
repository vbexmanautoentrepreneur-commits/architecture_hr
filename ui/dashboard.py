from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QTableWidget, QTableWidgetItem)
from PyQt6.QtWidgets import QMessageBox
from database.employee_repository import EmployeeRepository
from ui.add_employee_dialog import AddEmployeeDialog
from models.employee import Employee
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

class Dashboard(QWidget):

    def __init__(self):

        super().__init__()
        self.repo = EmployeeRepository()
        self.resize(1200, 700)
        self.setWindowTitle("RH Manager Pro")
        self.setWindowIcon(QIcon("icons/app.png"))
        self.build_ui()
        self.load_data()

    def build_ui(self):
        self.setStyleSheet("""
        QWidget { background:#f5f6fa; font-family:Segoe UI; font-size:11pt; }
        QTableWidget { background:white; border:1px solid #dcdde1; border-radius:8px; gridline-color:#ecf0f1; }
        QHeaderView::section { background:#3498db; color:white; padding:8px; border:none; font-weight:bold; }
        QPushButton { background:#3498db; color:white; border:none; border-radius:8px; padding:10px; min-width:120px; font-weight:bold; }
        QPushButton:hover { background:#2980b9; }
        QLineEdit { background:white; border:1px solid #dcdde1; border-radius:8px; padding:8px; }
         """)
        layout = QVBoxLayout()
        title = QLabel("RH Manager Pro")
        title.setStyleSheet(""" font-size:24px; font-weight:bold; """)
        layout.addWidget(title)
        kpi_layout = QHBoxLayout()
        self.lbl_effectif = QLabel()
        self.lbl_age = QLabel()
        self.lbl_salaire = QLabel()
        self.lbl_masse = QLabel()
        kpi_layout.addWidget(self.lbl_effectif)
        kpi_layout.addWidget(self.lbl_age)
        kpi_layout.addWidget(self.lbl_salaire)
        kpi_layout.addWidget(self.lbl_masse)
        layout.addLayout(kpi_layout)
        toolbar = QHBoxLayout()
        self.btn_add = QPushButton("Ajouter")
        self.btn_update = QPushButton("Modifier")
        self.btn_delete = QPushButton("Supprimer")
        toolbar.addWidget(self.btn_add)
        toolbar.addWidget(self.btn_update)
        toolbar.addWidget(self.btn_delete)
        layout.addLayout(toolbar)
        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.btn_quit = QPushButton("🚪 Quitter")
        self.btn_quit.setStyleSheet("""
        QPushButton {
            background-color: #e74c3c;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px;
            min-width: 120px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #c0392b;
        }

        QPushButton:pressed {
            background-color: #a93226;
        }
        """)
        layout.addWidget(self.btn_quit)

        self.setLayout(layout)
        self.btn_add.clicked.connect(self.add_employee)
        self.btn_delete.clicked.connect(self.delete_employee)
        self.btn_update.clicked.connect(self.update_employee)
        self.btn_quit.clicked.connect(self.quit_application)

    def quit_application(self):
            self.close()

    def closeEvent(self, event):

        reply = QMessageBox.question(
            self,
            "Quitter",
            "Voulez-vous vraiment quitter l'application ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

    def load_data(self):
        employees = self.repo.get_all()
        self.populate_table(employees)
        # self.lbl_status.setText(f"{len(employees)} ligne(s) chargée(s)")
        kpi = self.repo.get_kpis()
        self.lbl_effectif.setText(f"Effectif : {kpi['effectif']}")
        self.lbl_age.setText(f"Age moyen : {kpi['age_moyen']:.1f}" if kpi["age_moyen"] else "Age moyen : 0")
        self.lbl_salaire.setText(f"Salaire moyen : {kpi['salaire_moyen']:.0f} €" if kpi["salaire_moyen"] else "Salaire moyen : 0 €")
        self.lbl_masse.setText(f"Masse salariale : {kpi['masse']:.0f} €" if kpi["masse"] else "Masse salariale : 0 €")

    def populate_table(self, rows):
        self.table.clear()
        if not rows:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            return
        columns = list(rows[0].keys())
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        self.table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            for col_idx, column in enumerate(columns):
                value = row[column]
                if value is None: value = ""
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_idx, col_idx, item)
        self.table.resizeColumnsToContents()
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        if self.table.columnCount() > 0: self.table.horizontalHeader().setStretchLastSection(True)


    def add_employee(self):
        dlg = AddEmployeeDialog()
        if dlg.exec():
            data = dlg.get_data()
            employee = Employee(
                nom=data["nom"],
                age=data["age"],
                service=data["service"],
                salary=data["salary"],
                date_embauche=data["date_embauche"],
                email=data["email"],
                manager=data["manager"],
                telephone=data["telephone"],
                ville=data["ville"],
                pays=data["pays"],
                date_naissance=data["date_naissance"]
            )
            self.repo.add(employee)
            self.load_data()

    def update_employee(self):

        row = self.table.currentRow()
        if row < 0:
            return
        employee_id = int(self.table.item(row, 0).text())
        employee = self.repo.get_by_id(employee_id)
        if not employee:
            return
        dialog = AddEmployeeDialog(employee)
        if dialog.exec():
            data = dialog.get_data()
            updated_employee = Employee(
                nom=data["nom"],
                age=data["age"],
                service=data["service"],
                salary=data["salary"],
                date_embauche=data["date_embauche"],
                email=data["email"],
                manager=data["manager"],
                telephone=data["telephone"],
                ville=data["ville"],
                pays=data["pays"],
                date_naissance=data["date_naissance"],
                id=employee.id
            )
            self.repo.update(updated_employee)
            self.load_data()

    def delete_employee(self):

        row = self.table.currentRow()
        if row < 0: return
        employee_id = int(self.table.item(row, 0).text())
        self.repo.delete(employee_id)
        self.load_data()