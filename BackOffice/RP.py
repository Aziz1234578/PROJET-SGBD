import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QTabWidget, QComboBox, QScrollArea
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import mysql.connector

class ResponsableWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dashboard - Responsable Pédagogique")
        self.setFixedSize(600, 500)

        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="passer",
            database="Projet_sbgd"
        )

        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.tab_rapport = QWidget()
        self.tab_avis = QWidget()
        self.tab_point = QWidget()

        self.tab_widget.addTab(self.tab_rapport, "Rapport")  
        self.tab_widget.addTab(self.tab_avis, "Recueillir Avis")  
        self.tab_widget.addTab(self.tab_point, "Faire le Point")  

        self.configure_rapport_tab()
        self.configure_avis_tab()
        self.configure_point_tab()

    def configure_rapport_tab(self):
        layout = QVBoxLayout()
        self.tab_rapport.setLayout(layout)

        label_background = QLabel(self.tab_rapport)
        label_background.setPixmap(QPixmap("2.jpeg").scaled(self.tab_rapport.size())) 
        label_background.setGeometry(0, 0, self.tab_rapport.width(), self.tab_rapport.height()) 

        self.label_title_rapport = QLabel("Rapport Mensuel - Responsable Pédagogique", self.tab_rapport)
        self.label_title_rapport.setStyleSheet("font-size: 20px; font-weight: bold; color: #333; background-color: rgba(255, 255, 255, 0.7); border-radius: 10px;")
        self.label_title_rapport.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_title_rapport)

        self.label_classe = QLabel("Classe:", self.tab_rapport)
        self.label_classe.setStyleSheet("font-size: 16px; color: #333;")
        layout.addWidget(self.label_classe)

        self.combo_classe = QComboBox(self.tab_rapport)
        self.populate_combo_classe()
        self.combo_classe.setStyleSheet("font-size: 16px; border-radius: 5px; padding: 6px; background-color: white; border: 1px solid #ccc;")
        layout.addWidget(self.combo_classe)

        self.label_rapport = QLabel("Rapport:", self.tab_rapport)
        self.label_rapport.setStyleSheet("font-size: 16px; color: #333;")
        layout.addWidget(self.label_rapport)

        self.input_rapport = QTextEdit(self.tab_rapport)
        self.input_rapport.setStyleSheet("font-size: 16px; border: 1px solid #ccc; border-radius: 15px; padding: 6px; background-color: white;")
        layout.addWidget(self.input_rapport)

        self.button_enregistrer = QPushButton("Enregistrer", self.tab_rapport)
        self.button_enregistrer.setStyleSheet("background-color: #4CAF50; color: white; font-size: 18px; border-radius: 5px; padding: 8px;")
        self.button_enregistrer.clicked.connect(self.enregistrer_rapport)
        layout.addWidget(self.button_enregistrer)

    def populate_combo_classe(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT libelle FROM Classe")
        classes = cursor.fetchall()
        for classe in classes:
            self.combo_classe.addItem(classe[0])
        cursor.close()

    def enregistrer_rapport(self):
        classe = self.combo_classe.currentText()
        rapport = self.input_rapport.toPlainText()

        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO RapportRP (id_classe, contenu) VALUES ((SELECT id FROM Classe WHERE libelle = %s), %s)", (classe, rapport))
        self.db_connection.commit()
        cursor.close()

        QMessageBox.information(self, "Enregistrement réussi", "Le rapport a été enregistré avec succès.")

    def configure_avis_tab(self):
        layout = QVBoxLayout()
        self.tab_avis.setLayout(layout)

        label_background = QLabel(self.tab_avis)
        label_background.setPixmap(QPixmap("2.jpeg").scaled(self.tab_avis.size()))  
        label_background.setGeometry(0, 0, self.tab_avis.width(), self.tab_avis.height()) 

        label_title = QLabel("Avis des Étudiants - Responsable Pédagogique", self.tab_avis)
        label_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #333; background-color: rgba(255, 255, 255, 0.7); border-radius: 10px;")
        label_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(label_title)

        avis_scroll_area = QWidget(self.tab_avis)
        avis_scroll_area_layout = QVBoxLayout(avis_scroll_area)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(avis_scroll_area)
        layout.addWidget(scroll)

        cursor = self.db_connection.cursor()
        cursor.execute("SELECT Etudiant.nom, Etudiant.prenom, Classe.libelle, Avis.contenu FROM Etudiant JOIN Avis ON Etudiant.id = Avis.id_etudiant JOIN Classe ON Etudiant.id_classe = Classe.id")
        avis_data = cursor.fetchall()
        cursor.close()

        for nom, prenom, classe, contenu in avis_data:
            label_avis = QLabel(f"<b>{prenom} {nom} ({classe}) :</b><br>{contenu}", avis_scroll_area)
            label_avis.setStyleSheet("font-size: 16px; color: #333; background-color: rgba(255, 255, 255, 0.7); border-radius: 10px; padding: 10px;")
            label_avis.setWordWrap(True)
            avis_scroll_area_layout.addWidget(label_avis)

    def configure_point_tab(self):
        layout = QVBoxLayout()
        self.tab_point.setLayout(layout)

        label_background = QLabel(self.tab_point)
        label_background.setPixmap(QPixmap("2.jpeg").scaled(self.tab_point.size()))  
        label_background.setGeometry(0, 0, self.tab_point.width(), self.tab_point.height())  

        label_title = QLabel("Point sur l'exécution - Responsable Pédagogique", self.tab_point)
        label_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #333; background-color: rgba(255, 255, 255, 0.7); border-radius: 10px;")
        label_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(label_title)

        label_instructions = QLabel("Ici, Veuillez faire le point sur l'exécution des programmes", self.tab_point)
        label_instructions.setStyleSheet("font-size: 16px; color: #333; background-color: rgba(255, 255, 255, 0.7); border-radius: 10px;")
        label_instructions.setAlignment(Qt.AlignCenter)
        layout.addWidget(label_instructions)

        input_support = QTextEdit(self.tab_point)
        input_support.setStyleSheet("font-size: 16px; border: 1px solid #ccc; border-radius: 15px; padding: 6px; background-color: white;")
        layout.addWidget(input_support)

        button_save = QPushButton("Enregistrer", self.tab_point)
        button_save.setStyleSheet("background-color: #4CAF50; color: white; font-size: 18px; border-radius: 5px; padding: 8px;")
        button_save.clicked.connect(lambda: self.save_execution_point(input_support))
        layout.addWidget(button_save)

    def save_execution_point(self, input_support):
        execution_point = input_support.toPlainText()

        cursor = self.db_connection.cursor()
        query = "INSERT INTO PointExecution (id_rp, contenu) VALUES (%s, %s)"
        values = (1, execution_point)  
        cursor.execute(query, values)
        self.db_connection.commit()
        cursor.close()

        QMessageBox.information(self, "Enregistrement réussi", "Le point sur l'exécution a été enregistré avec succès.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ResponsableWindow()
    window.show()
    sys.exit(app.exec_())