import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QLabel, QDialog, QTextEdit
from PyQt5.QtGui import QPixmap
import mysql.connector
import os
from PyQt5.QtCore import Qt

class DirecteurWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Directeur des Études")
        self.setGeometry(300, 300, 500, 400)

        self.setStyleSheet("""
            QMainWindow {
                background-image: url('2.jpeg');
                background-color: #1E1E1E;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: 2px solid #4CAF50;
                border-radius: 15px;
                font-size: 18px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
        """)

        self.label_title = QLabel("Directeur des Études", self)
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setStyleSheet("font-size: 24px; font-weight: bold; color: black; margin-bottom: 20px;")
        self.label_title.setGeometry(0, 20, 500, 40)

        self.setup_buttons()

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
        self.central_widget = QVBoxLayout()
        self.central_widget.setAlignment(Qt.AlignCenter)

        button_pv = QPushButton("Voir PV", self)
        button_pv.clicked.connect(self.open_pdf)
        self.central_widget.addWidget(button_pv)

        button_rapport_rp = QPushButton("Voir Rapports RP", self)
        button_rapport_rp.clicked.connect(self.show_rapportrp_dialog)
        self.central_widget.addWidget(button_rapport_rp)

        button_compte_rendu = QPushButton("Voir Compte Rendu", self)
        button_compte_rendu.clicked.connect(self.show_compte_rendu)
        self.central_widget.addWidget(button_compte_rendu)

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

        rapportrp_dialog = RapportRPDialog([rapport[0] for rapport in rapportrp_data])
        rapportrp_dialog.setStyleSheet("""
            QDialog {
                background-color: #F0F0F0;
                width: 600px;
                height: 400px;
            }
            QTextEdit {
                font-size: 14px;
                border: 2px solid #ccc;
                border-radius: 10px;
                padding: 10px;
                background-color: white;
                width: 560px;
                height: 320px;
            }
        """)
        rapportrp_dialog.exec_()

    def show_compte_rendu(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT contenu FROM situationdept")
        compte_rendu_data = cursor.fetchall()

        if compte_rendu_data:
            compte_rendu_text = '\n'.join([row[0] for row in compte_rendu_data])
            compte_rendu_dialog = CompteRenduDialog(compte_rendu_text)
            compte_rendu_dialog.setStyleSheet("""
                QDialog {
                    background-color: #F0F0F0;
                    width: 600px;
                    height: 400px;
                }
                QTextEdit {
                    font-size: 14px;
                    border: 2px solid #ccc;
                    border-radius: 10px;
                    padding: 10px;
                    background-color: white;
                    width: 560px;
                    height: 320px;
                }
            """)
            compte_rendu_dialog.exec_()
        else:
            QMessageBox.warning(self, "Pas de Compte Rendu", "Aucun compte rendu trouvé dans la base de données.", QMessageBox.Ok)

        cursor.close()


class RapportRPDialog(QDialog):
    def __init__(self, rapports):
        super().__init__()

        self.setWindowTitle("Rapports RP")
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout(self)
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        for rapport in rapports:
            self.text_edit.append(rapport)

        layout.addWidget(self.text_edit)
        self.setLayout(layout)


class CompteRenduDialog(QDialog):
    def __init__(self, compte_rendu_text):
        super().__init__()

        self.setWindowTitle("Compte Rendu")
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout(self)
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setText(compte_rendu_text)

        layout.addWidget(self.text_edit)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DirecteurWindow()
    window.show()
    sys.exit(app.exec_())