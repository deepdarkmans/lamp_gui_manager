#!/usr/bin/env python3
# version 0.0.1
import sys
from PyQt5 import QtWidgets
from gui import design
import os
import subprocess


class appGUI(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.get_hosts()
        #
        self.chooseFolderButton.clicked.connect(self.browse_folder)
        self.chooseWWWButton.clicked.connect(self.browse_www_folder)
        self.createProjectButton.clicked.connect(self.create_host)
        self.refreshHostsButton.clicked.connect(self.get_hosts)

    def browse_folder(self):
        self.projrctFolderLine.clear()
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select folder")

        if directory:
            self.projrctFolderLine.setText(directory)

    def browse_www_folder(self):
        self.projrctWWWrLine.clear()
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select folder")
        if directory:
            self.projrctWWWrLine.setText(directory)

    def get_hosts(self):
        self.confArea.clear()
        hosts_folder = '/etc/apache2/sites-available/'
        if hosts_folder:
            for conf_name in os.listdir(hosts_folder):
                self.confArea.addItem(conf_name)

    def project_type_choose(self):
        if self.radioExistFolder.isChecked():
            return 1
        if self.radioGit.isChecked():
            return 2

    def create_host(self):
        project_name = self.projectNameLine.text()
        host_name = self.hostLine.text()
        project_folder = self.projrctFolderLine.text()
        www_folder = self.projrctWWWrLine.text()
        if (not project_name or project_name is None or host_name == '' or host_name is None or project_folder == '' or project_folder is None):
            QtWidgets.QMessageBox.about(self, "Error", "Not set:\nNo sudo pass\nProject name\nor\nHost name\nor\nProject folder")
        else:
            if self.project_type_choose() == 1:
                if (not www_folder or www_folder is None):
                    QtWidgets.QMessageBox.about(self, "Error", "Not set:\nProject www folder")
                else:
                    conf = open('/etc/apache2/sites-available/' + project_name + '.conf', 'w')
                    conf.write('<VirtualHost *:80>\nServerName ' + host_name + '\nServerAdmin webmaster@localhost\nDocumentRoot ' + www_folder + '\n<Directory \"' + www_folder + '\">\nAllowOverride All\nRequire all granted\n</Directory>\nErrorLog ${APACHE_LOG_DIR}/error.log\nCustomLog ${APACHE_LOG_DIR}/access.log combined\n</VirtualHost>')
                    conf.close()
                    os.system('a2ensite ' + project_name + '.conf')
                    os.system('systemctl reload apache2')
                    hosts = open('/etc/hosts', 'a')
                    hosts.write('127.0.0.1  ' + project_name + '.local\n')
                    hosts.close()
                    self.get_hosts()
                    QtWidgets.QMessageBox.about(self, "Success", "Success")
            elif self.project_type_choose() == 2:
                QtWidgets.QMessageBox.about(self, "Error", "Not set:\nProject www folder!!!!")
            else:
                QtWidgets.QMessageBox.about(self, "Error", "Not set:\nProject type")

    def set_sudo_pass(self):
        if os.geteuid() != 0:
            command = [sys.argv[0], sys.argv]
            os.execvp('sudo', ['sudo', 'python3'] + command)
        sudopass, ok = QtWidgets.QInputDialog.getText(self, 'Set Sudo Password', 'Sudo password:')
        if ok:
            return sudopass

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = appGUI()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()