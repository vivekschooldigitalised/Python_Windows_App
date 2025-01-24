import sys
from PyQt5.QtWidgets import ( # type: ignore
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QDialog,
    QLabel,
)
from PyQt5.QtWebEngineWidgets import QWebEngineView # type: ignore
from PyQt5.QtCore import QUrl # type: ignore


class PasswordDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Enter Security Code")
        self.setFixedSize(300, 150)

        # Dialog layout
        layout = QVBoxLayout()

        # Label
        label = QLabel("Enter the security code to close the exam browser:")
        layout.addWidget(label)

        # Password input field
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Buttons
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def get_password(self):
        """Return the entered password."""
        return self.password_input.text()


class ExamBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window Title
        self.setWindowTitle("Online Exam Tgs")

        # Fullscreen Mode
        self.showFullScreen()

        # Web View (Browser Window)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://lms.learningcurveapp.com/"))

        # Custom Close Button
        close_button = QPushButton("Click here to close the Online Exam Browser ❎")
        close_button.setStyleSheet(
            "font-size: 12px; padding: 10px; background-color: #696cff; color: white; border: none;"
        )
        close_button.clicked.connect(self.prompt_close_code)  # Connect button to prompt for the code

        # Layout for the button and browser
        button_layout = QHBoxLayout()
        button_layout.addWidget(close_button)
        button_layout.setContentsMargins(0, 0, 0, 0)  # Add some padding around the button

        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)  # Add button at the top
        main_layout.addWidget(self.browser)  # Add browser below

        # Main Widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Disable context menu (Right click)
        self.browser.setContextMenuPolicy(0)

        # Flag to allow closure
        self.can_close = False

    def prompt_close_code(self):
        """Prompt user to enter a code to close the application."""
        dialog = PasswordDialog()
        if dialog.exec_():  # If user clicks OK
            entered_code = dialog.get_password()
            correct_code = "2025"  # Set your secure code here

            if entered_code == correct_code:
                self.can_close = True  # Allow the application to close
                self.close_browser()
            else:
                QMessageBox.warning(self, "Incorrect Code", "The code you entered is incorrect. Try again.")

    def closeEvent(self, event):
        """Override the close event to prevent Alt + F4 unless explicitly allowed."""
        if not self.can_close:
            QMessageBox.warning(self, "Restricted Action", "You cannot close the application using Alt + F4.")
            event.ignore()  # Prevent the application from closing
        else:
            event.accept()  # Allow closure if the correct code was entered

    def close_browser(self):
        """Close the browser when the correct code is entered."""
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExamBrowser()
    window.show()
    sys.exit(app.exec_())