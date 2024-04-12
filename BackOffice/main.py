import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QComboBox, QMessageBox
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import mysql.connector

from membreDediee import PvEditorWindow  
from Coordinateur import CoordinateurWindow 
from RP import ResponsableWindow
from ChefDepartement import ChefDepartementWindow
from DirecteurEtudes import DirecteurWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Connexion")
        self.setFixedSize(600, 600)

        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="passer",
            database="Projet_sbgd"
        )

        background_label = QLabel(self)
        background_pixmap = QPixmap("2.jpeg")
        background_label.setPixmap(background_pixmap)
        background_label.setScaledContents(True)
        background_label.setGeometry(0, 0, 800, 600)

        self.label_title = QLabel("Connexion", self)
        self.label_title.setStyleSheet("color: black; font-size: 30px; font-weight: bold; margin-bottom: 20px;")
        self.label_title.setAlignment(Qt.AlignCenter)  

        logo_label = QLabel(self)
        logo_pixmap = QPixmap("logo.png")  
        logo_pixmap = logo_pixmap.scaledToWidth(200) 
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)

        self.label_username = QLabel("Nom d'utilisateur:", self)
        self.label_username.setStyleSheet("color: black; font-size: 20px; font-weight: bold;")

        self.input_username = QLineEdit(self)
        self.input_username.setStyleSheet("font-size: 16px; padding: 6px; border-radius: 5px; border: 1px solid #ccc;")
        self.input_username.setFixedWidth(300)

        self.label_password = QLabel("Mot de passe:", self)
        self.label_password.setStyleSheet("color: black; font-size: 20px; font-weight: bold;")

        self.input_password = QLineEdit(self)
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setStyleSheet("font-size: 16px; padding: 6px; border-radius: 5px; border: 1px solid #ccc;")
        self.input_password.setFixedWidth(300)

        self.combo_role = QComboBox(self)
        self.combo_role.addItems([
            "Chef de Département", "Membre Dédié", "Coordinateur Pédagogique",
            "Responsable Pédagogique", "Directeur des Études"
        ])
        self.combo_role.setStyleSheet("font-size: 16px; color: black;padding: 6px; border-radius: 5px; border: 1px solid #ccc;")
        self.combo_role.setFixedWidth(300)

        self.button_login = QPushButton("Se Connecter", self)
        self.button_login.setStyleSheet("background-color: #4CAF50; color: white; font-size: 18px; border-radius: 5px; padding: 8px;")
        self.button_login.setFixedWidth(300)

        layout = QVBoxLayout(self)
        layout.addWidget(logo_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.label_title, alignment=Qt.AlignCenter)
        layout.addWidget(self.label_username, alignment=Qt.AlignCenter)
        layout.addWidget(self.input_username, alignment=Qt.AlignCenter)
        layout.addWidget(self.label_password, alignment=Qt.AlignCenter)
        layout.addWidget(self.input_password, alignment=Qt.AlignCenter)
        layout.addWidget(self.combo_role, alignment=Qt.AlignCenter)
        layout.addWidget(self.button_login, alignment=Qt.AlignCenter)
        layout.addStretch(1)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.role_window = None

        self.button_login.clicked.connect(self.handle_login)

        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.setFont(font)

    def handle_login(self):
        username = self.input_username.text()
        password = self.input_password.text()
        selected_role = self.combo_role.currentText()

        cursor = self.db_connection.cursor()

        if selected_role == "Chef de Département":
            query = "SELECT * FROM ChefDepartement WHERE mail = %s AND mdp = %s"
            self.role_window = ChefDepartementWindow()             
        elif selected_role == "Membre Dédié":
            query = "SELECT * FROM membredediee WHERE mail = %s AND mdp = %s"
            self.role_window = PvEditorWindow() 
        elif selected_role == "Coordinateur Pédagogique":
            query = "SELECT * FROM coordinateurpedagogique WHERE mail = %s AND mdp = %s"
            self.role_window = CoordinateurWindow()  
        elif selected_role == "Responsable Pédagogique":
            query = "SELECT * FROM responsablepedagogique WHERE mail = %s AND mdp = %s"
            self.role_window = ResponsableWindow()            
        elif selected_role == "Directeur des Études":
            query = "SELECT * FROM directeuretudes WHERE mail = %s AND mdp = %s"
            self.role_window = DirecteurWindow()
            
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        if result:
            self.hide()
            self.role_window.show()
        else:
            QMessageBox.warning(self, "Erreur de connexion", "Nom d'utilisateur ou mot de passe incorrect.")

        cursor.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
