import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QComboBox, QMessageBox
from PyQt5.QtGui import QPixmap, QFont
import mysql.connector

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Application de Connexion")
        self.setFixedSize(800, 600)

        # Connexion à la base de données
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="passer",
            database="Projet_sbgd"
        )

        # Ajouter une image de fond à la fenêtre
        background_label = QLabel(self)
        background_pixmap = QPixmap("2.jpeg")
        background_label.setPixmap(background_pixmap)
        background_label.setScaledContents(True)  # Redimensionner l'image pour remplir toute la zone
        background_label.setGeometry(0, 0, 800, 600)

        # Création des widgets avec un style professionnel
        self.label_title = QLabel("Connexion", self)
        self.label_title.setStyleSheet("color: #333; font-size: 30px; font-weight: bold; margin-bottom: 20px;")

        self.label_username = QLabel("Nom d'utilisateur:", self)
        self.label_username.setStyleSheet("color: #333; font-size: 20px; font-weight: bold;")

        self.input_username = QLineEdit(self)
        self.input_username.setStyleSheet("font-size: 18px; padding: 10px; border-radius: 5px; border: 1px solid #ccc;")

        self.label_password = QLabel("Mot de passe:", self)
        self.label_password.setStyleSheet("color: #333; font-size: 20px; font-weight: bold;")

        self.input_password = QLineEdit(self)
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setStyleSheet("font-size: 18px; padding: 10px; border-radius: 5px; border: 1px solid #ccc;")

        self.combo_role = QComboBox(self)
        self.combo_role.addItems([
            "Chef de Département", "Membre Dédié", "Coordinateur Pédagogique",
            "Responsable Pédagogique", "Directeur des Études"
        ])
        self.combo_role.setStyleSheet("font-size: 18px; padding: 10px; border-radius: 5px; border: 1px solid #ccc;")

        self.button_login = QPushButton("Se Connecter", self)
        self.button_login.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px; border-radius: 5px; padding: 8px;")

        # Positionnement des widgets avec un layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.label_title)
        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.combo_role)
        layout.addWidget(self.button_login)
        layout.addStretch(1)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Connecter le bouton à une fonction
        self.button_login.clicked.connect(self.handle_login)

        # Utilisation d'une police de caractères personnalisée
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
        elif selected_role == "Membre Dédié":
            query = "SELECT * FROM MembreDediee WHERE mail = %s AND mdp = %s"
        elif selected_role == "Coordinateur Pédagogique":
            query = "SELECT * FROM CoordinateurPedagogique WHERE mail = %s AND mdp = %s"
        elif selected_role == "Responsable Pédagogique":
            query = "SELECT * FROM ResponsablePedagogique WHERE mail = %s AND mdp = %s"
        elif selected_role == "Directeur des Études":
            query = "SELECT * FROM DirecteurEtudes WHERE mail = %s AND mdp = %s"

        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        if result:
            QMessageBox.information(self, "Connexion réussie", f"Vous êtes connecté en tant que {selected_role}.")
        else:
            QMessageBox.warning(self, "Erreur de connexion", "Nom d'utilisateur ou mot de passe incorrect.")

        cursor.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
