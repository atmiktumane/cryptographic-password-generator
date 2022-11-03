from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys, string, random, pyperclip


ui,_ = loadUiType("userInterface.ui")  # This will load the main ui file

class MainApp(QMainWindow,ui):  # Class to create main window
    def __init__(self, parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Random Password Generator")
        self.UI()
        self.handle_button()
        self.generated_password = ""



    def UI(self): #Handel UI Changes
         style = open("darkTheme.css","r")
         style = style.read()
         self.setStyleSheet(style)


    def handle_button(self): # this will handle button interaction
        self.pushButton.clicked.connect(self.generate_password)
        self.pushButton_2.clicked.connect(self.copy_to_clipboard)


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


def main():  # Main function to execute app
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()