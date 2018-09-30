# Import the necessary modules required
import sys
import sys
from PySide2.QtWidgets import QApplication, QLabel
from PySide2.QtCore import Qt
# from PySide2.QtGui import QApplication, QLabel
# Main Function
if __name__ == '__main__':
    # Create the main application
    myApp = QApplication(sys.argv)
    # Create a Label and set its properties
    appLabel = QLabel()
    appLabel.setText("Hello, World!!!\n Look at my first app using PySide")
    appLabel.setAlignment(Qt.AlignCenter)
    appLabel.setWindowTitle("My First Application")
    appLabel.setGeometry(300, 300, 250, 175)
    # Show the Label
    appLabel.show()
    # Execute the Application and Exit
    myApp.exec_()
    sys.exit()