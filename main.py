#!/usr/bin/env python3
# version 0.0.1 dev
import sys
from PyQt5 import QtWidgets
from gui import design
import os
import controllers.sqlite_controller
import subprocess


def get_projects_data():
    return controllers.sqlite_controller.getDatabase()


def add_data(name, host_name, folder, www_folder, a2_conf, port, status):
    controllers.sqlite_controller.addData(name, host_name, folder, www_folder, a2_conf, port, status)


def get_server_info(server):
    result = subprocess.run(['systemctl', 'status', server, '|', 'grep', 'Active'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    lines = result.stdout
    result = lines.decode("utf-8")
    a = result.find('Active: ')
    status1 = result[a:]
    b = status1.find('(')
    status = status1[:b]
    c = status.find(': ')
    status = status[c:]
    status = status[1:]
    return status


def choose_project(it, col):
    return controllers.sqlite_controller.getProject(it.text(col))


def read_hosts():
    file = open('/etc/hosts', 'r')
    hosts = file.readlines()
    return hosts


def get_host_ip(host_name):
    rows = read_hosts()
    for row in rows:
        if host_name in row:
            host_name_find = row.find(host_name)
            ip = row[:host_name_find]
            return ip


def get_git_url(folder):
    try:
        file = open(folder + '/.git/config', 'r')
        config = file.readlines()
    except:
        return 'no git repository'
    for line in config:
        if 'url' in line:
            a = line.find('url = ')
            url = line[a:]
            url = url[6:]
            return url


class AppGui(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.get_hosts()
        # self.set_table()
        self.set_projects_tree()
        self.groupStatus = QtWidgets.QButtonGroup()
        self.groupStatus.addButton(self.radioButtonProjOn)
        self.groupStatus.addButton(self.radioButtonProjOff)
        self.groupCreate = QtWidgets.QButtonGroup()
        self.groupCreate.addButton(self.radioExistFolder)
        self.groupCreate.addButton(self.radioGit)
        self.groupFramework = QtWidgets.QButtonGroup()
        self.groupFramework.addButton(self.radioLuya)
        self.groupFramework.addButton(self.radioYii)
        self.groupFramework.addButton(self.radioWP)
        self.chooseFolderButton.clicked.connect(self.browse_folder)
        self.chooseWWWButton.clicked.connect(self.browse_www_folder)
        self.saveProjectButton.clicked.connect(self.create_edit_host)
        self.treeServersProjects.itemClicked.connect(self.fill_fields)
        self.radioExistFolder.toggled.connect(self.clear_fields)

        # self.refreshHostsButton.clicked.connect(add_data)

    def set_projects_tree(self):
        self.treeServersProjects.clear()
        apache = QtWidgets.QTreeWidgetItem(self.treeServersProjects, ['Apache'])
        mysql = QtWidgets.QTreeWidgetItem(self.treeServersProjects, ['MySQL'])
        self.treeServersProjects.addTopLevelItem(apache)
        self.treeServersProjects.addTopLevelItem(mysql)
        apache_status = get_server_info('apache2')
        mysql_status = get_server_info('mysql')
        apache_st = QtWidgets.QTreeWidgetItem(apache, [apache_status])
        mysql_st = QtWidgets.QTreeWidgetItem(mysql, [mysql_status])
        projects = get_projects_data()
        for row in projects:
            item = QtWidgets.QTreeWidgetItem(self.treeServersProjects, [row[1]])
            self.treeServersProjects.addTopLevelItem(item)
            QtWidgets.QTreeWidgetItem(item, ['host_name: ' + row[2]])
            QtWidgets.QTreeWidgetItem(item, ['folder: ' + row[3]])
            QtWidgets.QTreeWidgetItem(item, ['www: ' + row[4]])
            QtWidgets.QTreeWidgetItem(item, ['a2_conf: ' + row[5]])
            QtWidgets.QTreeWidgetItem(item, ['port: ' + str(row[6])])
            QtWidgets.QTreeWidgetItem(item, ['status: ' + str(row[7])])

    def fill_fields(self, it, col):
        if it.text(col) == 'Apache' or it.text(col) == 'MySQL':
            self.clear_fields()
            return
        data = choose_project(it, col)
        row = data[0]
        self.projectNameLine.setText(row[1])
        self.hostLine.setText(row[2])
        self.lineIP.setText(get_host_ip(row[2]))
        self.linePort.setText(str(row[6]))
        self.projrctFolderLine.setText(row[3])
        self.projrctWWWrLine.setText(row[4])
        self.groupStatus.setExclusive(False)
        self.radioButtonProjOn.setChecked(False)
        self.radioButtonProjOff.setChecked(False)
        self.groupStatus.setExclusive(True)
        self.groupCreate.setExclusive(False)
        self.radioExistFolder.setChecked(False)
        self.radioGit.setChecked(False)
        self.groupCreate.setExclusive(True)
        self.groupFramework.setExclusive(False)
        self.radioLuya.setChecked(False)
        self.radioYii.setChecked(False)
        self.radioWP.setChecked(False)
        self.groupFramework.setExclusive(True)
        self.repositoryLine.setText(get_git_url(row[3]))
        if row[7] == 1:
            self.radioButtonProjOn.setChecked(True)
        if row[7] == 0:
            self.radioButtonProjOff.setChecked(True)
        if row[9] == 1:
            self.radioLuya.setChecked(True)
        if row[9] == 2:
            self.radioYii.setChecked(True)
        if row[9] == 3:
            self.radioWP.setChecked(True)

    def clear_fields(self):
        self.projectNameLine.clear()
        self.hostLine.clear()
        self.lineIP.setText('127.0.0.1')
        self.linePort.setText('80')
        self.projrctFolderLine.clear()
        self.projrctWWWrLine.clear()
        self.repositoryLine.clear()
        self.groupStatus.setExclusive(False)
        self.radioButtonProjOn.setChecked(False)
        self.radioButtonProjOff.setChecked(False)
        self.groupStatus.setExclusive(True)
        self.groupFramework.setExclusive(False)
        self.radioLuya.setChecked(False)
        self.radioYii.setChecked(False)
        self.radioWP.setChecked(False)
        self.groupFramework.setExclusive(True)

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

    def project_create_from(self):
        if self.radioExistFolder.isChecked():
            return 1
        if self.radioGit.isChecked():
            return 2
        return 0

    def create_edit_host(self):
        project_name = self.projectNameLine.text()
        git = self.repositoryLine.text()
        host_name = self.hostLine.text()
        ip = self.lineIP.text()
        port = self.linePort.text()
        project_folder = self.projrctFolderLine.text()
        www_folder = self.projrctWWWrLine.text()
        action = self.project_create_from()
        if not project_name or project_name is None or host_name == '' or host_name is None or project_folder == '' or \
                project_folder is None:
            QtWidgets.QMessageBox.about(self, "Error", "Not set:\nNo sudo pass\nProject name\nor\nHost "
                                                       "name\nor\nProject folder")
        else:
            conf_file = '<VirtualHost *:' + port + '>\nServerName ' + host_name + '\nServerAdmin\nwebmaster@localhost' \
                                                                                  '\nDocumentRoot ' + www_folder + \
                        '\n<Directory \"' + www_folder + '\">\nAllowOverride All\nRequire all ' \
                                                         'granted\n</Directory>\nErrorLog ${' \
                                                         'APACHE_LOG_DIR}/error.log\nCustomLog ${' \
                                                         'APACHE_LOG_DIR}/access.log combined\n</VirtualHost> '
            if action == 1:
                if not www_folder or www_folder is None:
                    QtWidgets.QMessageBox.about(self, "Error", "Not set:\nProject www folder")
                else:
                    conf = open('/etc/apache2/sites-available/' + project_name + '.conf', 'w')
                    conf.write(conf_file)
                    conf.close()
                    os.system('a2ensite ' + project_name + '.conf')
                    os.system('systemctl reload apache2')
                    hosts = open('/etc/hosts', 'a')
                    hosts.write(ip + ' ' + host_name + '\n')
                    hosts.close()
                    add_data(project_name, host_name, project_folder, www_folder, project_name + '.conf', int(port), 1)
                    QtWidgets.QMessageBox.about(self, "Success", "Success")
                    self.set_projects_tree()
            elif action == 2:
                QtWidgets.QMessageBox.about(self, "Error", "Not set:\nProject www folder!!!!")
            elif action == 0:
                os.system('a2dissite ' + project_name + '.conf')
                os.system('systemctl reload apache2')
                os.system('rm /etc/apache2/sites-available/' + project_name + '.conf')
                hosts_file = open('/etc/hosts', 'r')
                hosts_rows = hosts_file.readlines()
                hosts_file.close()
                os.system('rm /etc/hosts')
                for row in hosts_rows:
                    if host_name in row:
                        continue
                    hosts = open('/etc/hosts', 'a')
                    hosts.write(row)
                    hosts.close()
                conf = open('/etc/apache2/sites-available/' + project_name + '.conf', 'w')
                conf.write(conf_file)
                conf.close()
                os.system('a2ensite ' + project_name + '.conf')
                os.system('systemctl reload apache2')
                hosts = open('/etc/hosts', 'a')
                hosts.write(ip + ' ' + host_name + '\n')
                hosts.close()
                add_data(project_name, host_name, project_folder, www_folder, project_name + '.conf', int(port), 1)
                QtWidgets.QMessageBox.about(self, "Success", "Success")
                self.set_projects_tree()
            else:
                QtWidgets.QMessageBox.about(self, "Error", "Error!!!")

    def set_sudo_pass(self):
        if os.geteuid() != 0:
            command = [sys.argv[0], sys.argv]
            os.execvp('sudo', ['sudo', 'python3'] + command)
        surpass, ok = QtWidgets.QInputDialog.getText(self, 'Set Sudo Password', 'Sudo password:')
        if ok:
            return surpass


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = AppGui()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
