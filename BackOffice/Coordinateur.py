import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QComboBox
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import mysql.connector

class CoordinateurWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rapport Mensuel - Coordinateur Pédagogique")
        self.setFixedSize(700, 550)

        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="passer",
            database="Projet_sbgd"
        )

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.label_background = QLabel(self.central_widget)
        self.label_background.setPixmap(QPixmap("2.jpeg").scaled(self.size()))  # Ajustement de la taille de l'image
        self.label_background.setGeometry(0, 0, 700, 550)

        self.label_title = QLabel("Rapport Mensuel - Coordinateur Pédagogique", self.central_widget)
        self.label_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333; background-color: rgba(255, 255, 255, 0.7); border-radius: 10px;")
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setGeometry(50, 50, 600, 40)

        self.label_classe = QLabel("Classe:", self.central_widget)
        self.label_classe.setStyleSheet("font-size: 16px; color: #333;")
        self.label_classe.setGeometry(50, 120, 200, 40)

        self.combo_classe = QComboBox(self.central_widget)
        self.populate_combo_classe()
        self.combo_classe.setStyleSheet("font-size: 16px; border-radius: 5px; padding: 6px; background-color: white;")
        self.combo_classe.setGeometry(200, 120, 300, 40)

        self.label_rapport = QLabel("Rapport:", self.central_widget)
        self.label_rapport.setStyleSheet("font-size: 16px; color: #333;")
        self.label_rapport.setGeometry(50, 180, 200, 30)

        self.input_rapport = QTextEdit(self.central_widget)
        self.input_rapport.setStyleSheet("font-size: 16px; border: 1px solid #ccc; border-radius: 15px; padding: 6px; background-color: white;")
        self.input_rapport.setGeometry(50, 220, 600, 300)  
       
        self.button_enregistrer = QPushButton("Enregistrer", self.central_widget)
        self.button_enregistrer.setStyleSheet("background-color: #4CAF50; color: white; font-size: 18px; border-radius: 5px; padding: 8px;")
        self.button_enregistrer.setGeometry(280, 450, 150, 40)
        self.button_enregistrer.clicked.connect(self.enregistrer_rapport)

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
        cursor.execute("INSERT INTO RapportCoordinateur (id_classe, contenu) VALUES ((SELECT id FROM Classe WHERE libelle = %s), %s)", (classe, rapport))
        self.db_connection.commit()
        cursor.close()

        QMessageBox.information(self, "Enregistrement réussi", "Le rapport a été enregistré avec succès.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoordinateurWindow()
    window.show()
    sys.exit(app.exec_())
