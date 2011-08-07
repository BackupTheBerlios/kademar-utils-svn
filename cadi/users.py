#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from commands import getoutput
from os import path, system

#import funcions_k

from ui_users import Ui_FormUsers as Ui_Form

class panelUsers(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        global tipus
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pages.setCurrentIndex(0)

        self.userIcon="/usr/share/kademar/utils/cadi/img/user.png"
        self.userRootIcon="/usr/share/kademar/utils/cadi/img/user-password.png"

#####  SIGNAL & SLOTS  #####
        self.connect(self.ui.b_sortir, SIGNAL("clicked()"), self.close)
        self.connect(self.ui.b_cancel, SIGNAL("clicked()"), self.boto_cancel)
        self.connect(self.ui.b_create, SIGNAL("clicked()"), self.boto_create)
        self.connect(self.ui.b_delUser, SIGNAL("clicked()"), self.boto_delUser)
        self.connect(self.ui.b_addUser, SIGNAL("clicked()"), self.boto_newUser)
        self.connect(self.ui.list_user, SIGNAL(" currentRowChanged (int)"), self.enable_delUserButton)
        self.connect(self.ui.b_modifyUser, SIGNAL("clicked()"), self.boto_modifyUser)
        self.connect( self.ui.ch_pass, SIGNAL("stateChanged (int)"), self.changeModifyPass)
        self.connect( self.ui.ch_username, SIGNAL("stateChanged (int)"), self.changeModifyUser)
        self.connect(self.ui.b_cancel_2, SIGNAL("clicked()"), self.main)
        self.connect(self.ui.b_modify, SIGNAL("clicked()"), self.saveModifications)
#### END SIGNAL & SLOTS ####

        self.reloadUserList()

    def main(self):
        self.ui.pages.setCurrentIndex(0)

    def changeModifyUser(self, num):
        if num==2:
            num=1
        self.ui.le_modify_user.setVisible(num)
        self.ui.l_user.setVisible(num)

    def changeModifyPass(self, num):
        if num==2:
            num=1
        self.ui.le_modify_pass.setVisible(num)
        self.ui.l_pass.setVisible(num)

    def enable_delUserButton(self, num):
        self.ui.l_warn.setVisible(0)
        if num==0:
            self.ui.b_delUser.setEnabled(0)
            self.userSelected=self.uids[num][1]
            self.uidSelected=self.uids[num][0]
            self.ui.l_warn.setText(self.tr("Root user cannot be deleted"))
            self.ui.l_warn.setVisible(1)
        else:
            self.userSelected=self.uids[num][1]
            self.uidSelected=self.uids[num][0]
            if not getoutput("users | grep "+str(self.userSelected)):
                self.ui.b_delUser.setEnabled(1)
            else:
                self.ui.b_delUser.setEnabled(0)
                self.ui.l_warn.setText(self.tr("Selected user it's logged in"))
                self.ui.l_warn.setVisible(1)
        #print self.userSelected

    def reloadUserList(self):
        #global uids,uidslliures
        #cuenta:password:uid:gid:gecos:home:bash
        self.ui.list_user.clear()
        self.uids = []
        self.llista=[]
        self.uidslliures=[]
        for l in open('/etc/passwd'):
            self.campos = l.split(':')
            if (int(self.campos[2])==0) or (int(self.campos[2])>999) and (int(self.campos[2])<60000):
                self.llista.append(int(self.campos[2]))
                self.llista.append(self.campos[0])
                self.uids.append(self.llista)
                self.llista=[]

        for i in range(len(self.uids)):
            a=QListWidgetItem(self.ui.list_user)

            if self.uids[i][1].strip().lower()=='root':
                a.setIcon(QIcon(self.userRootIcon))
            else:
                a.setIcon(QIcon(self.userIcon))
            
            a.setText(self.uids[i][1].strip())
            self.ui.list_user.addItem(a)
            #if self.uids[i][1].strip().lower()<>'root':
                #a=QListWidgetItem(self.ui.list_user)
                #a.setText(self.uids[i][1].strip())
                #a.setIcon(QIcon(self.userIcon))
                #self.ui.list_user.addItem(a)
        self.uidsocupats=[]
        for i in self.uids:
            self.uidsocupats.append(i[0])
        for i in range(1000,2000):
            if i not in self.uidsocupats:
                self.uidslliures.append(i)
        self.ui.b_delUser.setEnabled(0)

    def boto_delUser(self):
        self.userToRemove=self.userSelected
        if self.userToRemove.lower()=="root":
            QMessageBox.critical(self, self.tr("User Delete Error!"), self.tr("Root (Administrator) user cannot be removed."), QMessageBox.Ok)
        else:
            if QMessageBox.critical(self, self.tr("Delete User Question"), self.tr("Are you sure to delete %s user.\n Be sure, because this acction cannot be back." %(self.userToRemove) ) , QMessageBox.No, QMessageBox.Ok) == QMessageBox.Ok:
                system("deluser "+str(self.userToRemove)) #user deletion
                if QMessageBox.critical(self, self.tr("Delete User Data?"), self.tr("Do you want to remove all user data on his home?.\n Be sure, because this acction cannot be back.") , QMessageBox.No, QMessageBox.Ok) == QMessageBox.Ok:
                    system("rm -fr /home/"+str(self.userToRemove))
                
                self.ui.pages.setCurrentIndex(0)
                self.reloadUserList()
            

    def boto_newUser(self):
        self.ui.pages.setCurrentIndex(1)
        for i in [ self.ui.le_user, self.ui.le_login, self.ui.le_passwd, self.ui.le_passwd2 ]:
            i.setText("")

    def boto_cancel(self):
        self.ui.pages.setCurrentIndex(0)

    def boto_create(self):
        password=self.ui.le_passwd.text()
        uid=self.uidslliures[0]
        gid=100
        gecos=str(self.ui.le_login.text()).strip().lower().title()
        cuenta=self.ui.le_login.text()
        home='/home/'+cuenta
        bash='/bin/bash'
        if not path.exists(home):
            crea_home="creahome_si"
            print "Crea Home SI"
        else:
            crea_home="creahome_no"
            print "Crea Home NO"
        linia=cuenta+':'+password+':'+str(uid)+':'+str(gid)+':'+gecos+':'+home+':'+bash
        system('echo '+str(linia)+'  > /tmp/usu.txt')
        system('/usr/sbin/newusers /tmp/usu.txt')
        system('rm -f /tmp/usu.txt')
        QApplication.processEvents()
        #Si el path no existeix, vol dir que l'usuari es NOU, sino esta sobreescriguent un usuari antic, llavors no tocarem res
        if crea_home=="creahome_si":
            system('mkdir -p "'+str(home)+'"')
            QApplication.processEvents()
            system('cp -Rfr /etc/skel/* '+str(home)+'\n')
            QApplication.processEvents()
            system('cp -Rfr /etc/skel/.??* '+str(home)+'\n')
        print "Home='"+str(home)+"'"
        QApplication.processEvents()

        #Script per ultimar la creació del perfil d'usuari
        print 'sh scripts/crea_perfil_usuari '+str(cuenta)+' '+str(crea_home)
        system('sh scripts/crea_perfil_usuari '+str(cuenta)+' "'+str(crea_home)+'"')
        self.ui.pages.setCurrentIndex(0)
        self.reloadUserList()
        
    def boto_modifyUser(self):
      #initial preparation
        self.ui.le_modify_pass.setText("")
        self.ui.le_modify_user.setText(getoutput('grep '+str(self.uidSelected)+': /etc/passwd | grep '+str(self.userSelected)+' | cut -d: -f5'))
        for i in [ self.ui.le_modify_pass, self.ui.le_modify_user, self.ui.l_user, self.ui.l_pass ]:
            i.setVisible(0)
        self.ui.ch_pass.setChecked(0)
        self.ui.ch_username.setChecked(0)
        self.ui.pages.setCurrentIndex(2)
        
        
    def saveModifications(self):
        if self.ui.ch_pass.isChecked():
            system("sh scripts/change_user_password "+str(self.userSelected)+" '"+str(self.ui.le_modify_pass.text())+"'")

        if self.ui.ch_username.isChecked():
            self.nounom=self.ui.le_modify_user.text()
            if self.nounom<>"":
                system('sed s,"`grep '+str(self.uidSelected)+': /etc/passwd | grep '+str(self.userSelected)+' | cut -d: -f5`","'+str(self.nounom)+'",g -i /etc/passwd')
        self.ui.pages.setCurrentIndex(0)
        self.reloadUserList()

#app = QApplication(sys.argv)
#preferencies = preferencies()
#preferencies.show()
#app.exec_()