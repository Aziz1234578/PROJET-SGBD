import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QFrame
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from textwrap import fill
import qrcode
import mysql.connector 

class PvEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rédaction du PV")
        self.setFixedSize(600, 500)  


        self.setStyleSheet("QMainWindow { background-image: url(2.jpeg); background-size: cover; }")

        self.label_welcome = QLabel("Bienvenue dans votre Espace Personnel.\n", self)
        self.label_welcome.setAlignment(Qt.AlignCenter)

        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        self.label_welcome.setFont(font)

        self.label_date = QLabel("<b>Date de la séance:</b>", self)
        self.input_date = QTextEdit(self)
        self.input_date.setStyleSheet("font-size: 14px; padding: 6px; border-radius: 5px; border: 1px solid #ccc;")

        self.label_content = QLabel("<b>Contenu du PV:</b>", self)
        self.input_content = QTextEdit(self)
        self.input_content.setStyleSheet("font-size: 14px; padding: 6px; border-radius: 5px; border: 1px solid #ccc;")

        self.label_decisions = QLabel("<b>Décisions du conseil:</b>", self)
        self.input_decisions = QTextEdit(self)
        self.input_decisions.setStyleSheet("font-size: 14px; padding: 6px; border-radius: 5px; border: 1px solid #ccc;")

        self.button_save = QPushButton("Enregistrer et Générer PDF", self)
        self.button_save.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px; border-radius: 5px; padding: 8px;")
        self.button_save.clicked.connect(self.save_and_generate_pdf)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label_welcome)
        layout.addWidget(QFrame(self)) 
        layout.addWidget(self.label_date)
        layout.addWidget(self.input_date)
        layout.addWidget(QFrame(self))  
        layout.addWidget(self.label_content)
        layout.addWidget(self.input_content)
        layout.addWidget(QFrame(self))  
        layout.addWidget(self.label_decisions)
        layout.addWidget(self.input_decisions)
        layout.addWidget(QFrame(self))  
        layout.addWidget(self.button_save)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.setFont(font)

        self.input_date.setPlaceholderText("Entrez la date ici")
        self.input_content.setPlaceholderText("Saisissez le contenu du PV ici")
        self.input_decisions.setPlaceholderText("Ajoutez les décisions du conseil ici")

        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="passer",
            database="projet_sbgd"
        )

    def wrap_text(self, text, max_width):
        wrapped_text = fill(text, max_width)
        return wrapped_text

    def save_and_generate_pdf(self):
        date = self.input_date.toPlainText()
        content = self.wrap_text(self.input_content.toPlainText(), 90)
        decisions = self.wrap_text(self.input_decisions.toPlainText(), 90)

        pdf_path = "PV_Commission_Pedagogique.pdf"
        c = canvas.Canvas(pdf_path, pagesize=letter)

        title = "Procès-verbal de la Commission Pédagogique"
        title_width = c.stringWidth(title, "Helvetica-Bold", 16) 
        title_x = (c._pagesize[0] - title_width) / 2
        c.setFont("Helvetica-Bold", 16)
        c.drawString(title_x, 750, title)

        c.setFont("Helvetica", 12)
        c.drawString(50, 720, f"Date de la séance: {date}")

        c.drawString(50, 690, "Contenu du PV:")
        text_lines = content.split('\n')
        y_position = 670
        for line in text_lines:
            if y_position < 50:
                c.showPage()
                y_position = 750
                c.setFont("Helvetica-Bold", 16)
                c.drawString(title_x, 750, title)
                c.setFont("Helvetica", 12)
                c.drawString(50, 720, f"Date de la séance: {date}")
            c.drawString(50, y_position, line)
            y_position -= 20

        c.drawString(50, y_position - 20, "Décisions du conseil:")
        decisions_lines = decisions.split('\n')
        y_position -= 40
        for line in decisions_lines:
            if y_position < 20:
                c.showPage()
                y_position = 750
                c.setFont("Helvetica-Bold", 16)
                c.drawString(title_x, 750, title)
                c.setFont("Helvetica", 12)
                c.drawString(50, 720, f"Date de la séance: {date}")
            c.drawString(50, y_position, line)
            y_position -= 20
        logo_path = "logo.png"
        logo_width = 100
        logo_height = 100
        bottom_right_x = c._pagesize[0] - 50 - logo_width
        bottom_right_y = 160
        c.drawImage(logo_path, bottom_right_x, bottom_right_y, width=logo_width, height=logo_height)

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(pdf_path)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_img.save("qrcode.png")

        c.drawImage("qrcode.png", 50, 160, width=100, height=100)

        c.save()

        cursor = self.db_connection.cursor()
        query = "INSERT INTO pv (pdf_adresse) VALUES (%s)"
        cursor.execute(query, (pdf_path,))
        self.db_connection.commit()
        cursor.close()

        QMessageBox.information(self, "Enregistrement réussi", "Votre PV a bien été enregistré.", QMessageBox.Ok)

        print(f"PV enregistré et PDF généré avec succès à {pdf_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PvEditorWindow()
    window.show()
    sys.exit(app.exec_())