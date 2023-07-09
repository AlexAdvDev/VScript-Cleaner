import sys
import subprocess
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QStyle
import PyQt5

foundP2 = False
if os.path.exists("C:\SteamLibrary\steamapps\common\Portal 2"):
    foundP2 = True
    P2Directory = "C:\SteamLibrary\steamapps\common\Portal 2"
if os.path.exists("C:\Program Files\Steam\steamapps\common\Portal 2"):
    foundP2 = True
    P2Directory = "C:\Program Files\Steam\steamapps\common\Portal 2"
if os.path.exists("C:\Program Files (x86)\Steam\steamapps\common\Portal 2"):
    foundP2 = True
    P2Directory = "C:\Program Files (x86)\Steam\steamapps\common\Portal 2"
if not foundP2:
    P2Directory = input("Portal 2 not automatically found! Please enter your Portal 2 directory: ")

class GameLauncher(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Portal 2 VScript Launcher")
        self.setGeometry(300, 300, 325, 200)

        self.button_with_scripts = QPushButton("Launch with VScripts", self)
        self.button_with_scripts.setGeometry(50, 50, 200, 50)
        self.button_with_scripts.clicked.connect(self.launch_with_scripts)

        self.button_without_scripts = QPushButton("Launch without VScripts", self)
        self.button_without_scripts.setGeometry(50, 100, 200, 50)
        self.button_without_scripts.clicked.connect(self.launch_without_scripts)

    def launch_with_scripts(self):
        cwd = os.path.dirname(os.path.realpath(__file__))
        os.system("python " + os.path.join(cwd, "vscriptmanager.py") + " -o import")
        subprocess.Popen([os.path.join(P2Directory, "portal2.exe"), '-novid'])

    def launch_without_scripts(self):
        cwd = os.path.dirname(os.path.realpath(__file__))
        print(os.path.join(P2Directory, "portal2.exe"))
        os.system("python " + os.path.join(cwd, "vscriptmanager.py") + " -o extract")
        subprocess.Popen([os.path.join(P2Directory, "portal2.exe"), '-novid'])



if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = GameLauncher()
    launcher.show()
    sys.exit(app.exec_())
