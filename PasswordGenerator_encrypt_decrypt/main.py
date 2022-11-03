from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys, string, random, pyperclip
from cryptography.fernet import Fernet


ui,_ = loadUiType("userInterface.ui")  # This will load the main ui file

class MainApp(QMainWindow,ui):  # Class to create main window
    def __init__(self, parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Password Generator")
        self.UI()
        self.handle_button()
        self.generated_password = ""
        self.loaded_key = ""



    def UI(self): #Handel UI Changes
         style = open("darkTheme.css","r")
         style = style.read()
         self.setStyleSheet(style)


    def handle_button(self): # this will handle button interaction
        self.pushButton.clicked.connect(self.generate_password)
        self.pushButton_2.clicked.connect(self.copy_to_clipboard)
        self.pushButton_5.clicked.connect(self.generate_thekey)
        self.pushButton_6.clicked.connect(self.load_key)
        self.pushButton_3.clicked.connect(self.encrypt_message)
        self.pushButton_4.clicked.connect(self.decrypt_message)


    def generate_password(self):
        chars = string.ascii_letters + string.digits + string.punctuation
        password_length = self.spinBox.value()
        self.generated_password = ""
        for c in range(password_length):
            self.generated_password += random.choice(chars)

        self.textBrowser.setText(self.generated_password)


    def copy_to_clipboard(self):
        pyperclip.copy(self.generated_password)
        # pyperclip.paste() # used for pasting
        self.label_3.setText("Copied!")


    def generate_thekey(self):
        file_name = self.lineEdit.text()
        if file_name=="":
            QMessageBox.about(self, "Error", "Key File Name is missing")
        else:
            key = Fernet.generate_key()
            with open(file_name, "wb") as key_file:
                key_file.write(key)

            self.label_3.setText("Key Generated and Saved")


    def load_key(self):
        file_name = self.lineEdit.text()
        with open(file_name, "rb") as f:
            self.loaded_key = f.readline()

        self.label_3.setText("Key Loaded")

    def encrypt_message(self):
        if self.loaded_key=="" and self.generated_password=="":
            QMessageBox.about(self, "Error", "Key or Generated password is missing")
        else:
            encoded_message = self.generated_password.encode()
            f = Fernet(self.loaded_key)
            encrypted_message = f.encrypt(encoded_message)

            file_name = self.lineEdit_2.text()
            with open(file_name, "wb") as file:
                file.write(encrypted_message)

            file.close()

            self.label_3.setText("Password Encrypted & Saved")


    def decrypt_message(self):
        if self.loaded_key!="":
            key = self.loaded_key
            f = Fernet(key)

            file_name = self.lineEdit_2.text()
            with open(file_name, "rb") as file:
                encrypted_message = file.readline()

            file.close()

            decrypted_message = f.decrypt(encrypted_message)

            password = decrypted_message.decode()

            self.textBrowser_3.setText(password)
            self.label_3.setText("File Decrypted")
        else:
            QMessageBox.about(self, "Error", "Key Not Loaded")



def main():  # Main function to execute app
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()