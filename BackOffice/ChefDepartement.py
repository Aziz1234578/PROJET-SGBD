import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QTextEdit, QWidget, QMessageBox, QDialog
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
import mysql.connector
import os

class RapportRPDialog(QDialog):
    def __init__(self, rapports):
        super().__init__()
        self.setWindowTitle("Rapports RP")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label_title = QLabel("Rapports du Responsable Pédagogique", self)
        self.label_title.setFont(QFont("Arial", 18, QFont.Bold))
        self.label_title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label_title)

        self.textedit_rapports = QTextEdit(self)
        self.textedit_rapports.setReadOnly(True)
        self.layout.addWidget(self.textedit_rapports)

        self.display_rapports(rapports)

        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QLabel {
                font-size: 18px;
                color: #333333;
                margin-bottom: 10px;
            }
            QTextEdit {
                font-size: 14px;
                padding: 10px;
                border: 1px solid #cccccc;
                border-radius: 5px;
                background-color: #ffffff;
            }
        """)

    def display_rapports(self, rapports):
        rapport_text = "\n\n".join(rapports)
        self.textedit_rapports.setText(rapport_text)
        self.textedit_rapports.setFont(QFont("Arial", 12))


class ChefDepartementWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Espace Chef de Département")
        self.setGeometry(100, 100, 700, 500)

        # Définir une icône pour la fenêtre
        self.setWindowIcon(QIcon('icon.png'))

        # Style CSS pour la fenêtre principale
        self.setStyleSheet("""
            QMainWindow {
                background-image: url('2.jpeg');
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 18px;
                color: #333333;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QTextEdit {
                font-size: 14px;
                padding: 5px;
                border: 1px solid #cccccc;
            }
        """)

        self.central_widget = QVBoxLayout()
        self.central_widget.setAlignment(Qt.AlignTop)

        self.label_title = QLabel("Espace Chef de Département", self)
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        self.central_widget.addWidget(self.label_title)

        self.setup_buttons()
        self.setup_rapport_textedit()
        self.setup_save_button()

        central_widget = QWidget(self)
        central_widget.setLayout(self.central_widget)
        self.setCentralWidget(central_widget)

        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="passer",
            database="Projet_sbgd"
        )

    def setup_buttons(self):
        button_pv = QPushButton("Voir PV", self)
        button_pv.clicked.connect(self.open_pdf)
        button_pv.setStyleSheet("margin-right: 10px;")
        self.central_widget.addWidget(button_pv)

        button_rapport_rp = QPushButton("Voir Rapports RP", self)
        button_rapport_rp.clicked.connect(self.show_rapportrp_dialog)
        self.central_widget.addWidget(button_rapport_rp)

    def open_pdf(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT pdf_adresse FROM pv LIMIT 1")
        pdf_data = cursor.fetchone()
        cursor.close()

        if pdf_data:
            pdf_path = pdf_data[0]
            if os.path.exists(pdf_path):
                os.system(f'start {pdf_path}')
            else:
                QMessageBox.warning(self, "Fichier PDF introuvable", "Le fichier PDF n'existe pas.", QMessageBox.Ok)
        else:
            QMessageBox.warning(self, "Pas de PV", "Aucun PV trouvé dans la base de données.", QMessageBox.Ok)

    def show_rapportrp_dialog(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT contenu FROM rapportrp")
        rapportrp_data = cursor.fetchall()
        cursor.close()

        if rapportrp_data:
            rapports = [rapport[0] for rapport in rapportrp_data]
            rapportrp_dialog = RapportRPDialog(rapports)
            rapportrp_dialog.exec_()
        else:
            QMessageBox.warning(self, "Pas de Rapports RP", "Aucun rapport RP trouvé dans la base de données.", QMessageBox.Ok)

    def setup_rapport_textedit(self):
        self.label_rapport = QLabel("Compte Rendu du Chef de Département:", self)
        self.label_rapport.setStyleSheet("font-size: 18px; color: #333333; margin-top: 20px;")
        self.central_widget.addWidget(self.label_rapport)

        self.textedit_rapport = QTextEdit(self)
        self.central_widget.addWidget(self.textedit_rapport)

    def setup_save_button(self):
        button_save = QPushButton("Enregistrer et Transmettre", self)
        button_save.clicked.connect(self.save_and_transmit_report)
        self.central_widget.addWidget(button_save)

    def save_and_transmit_report(self):
        contenu_rapport = self.textedit_rapport.toPlainText()
        if contenu_rapport.strip():
            cursor = self.db_connection.cursor()
            cursor.execute("INSERT INTO situationdept (contenu) VALUES (%s)", (contenu_rapport,))
            self.db_connection.commit()
            cursor.close()
            QMessageBox.information(self, "Rapport Enregistré",
                                    "Le rapport a été enregistré et transmis avec succès au Chef du Département.",
                                    QMessageBox.Ok)
        else:
            QMessageBox.warning(self, "Rapport Vide", "Veuillez saisir le rapport avant de l'enregistrer et de le transmettre.",
                                QMessageBox.Ok)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChefDepartementWindow()
    window.show()
    sys.exit(app.exec_())
