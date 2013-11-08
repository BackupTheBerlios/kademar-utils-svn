#!/usr/bin/python

#
# Kademar Bitnami Control Panel is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Kademar Bitnami Control Panel is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Kademar Bitnami Control Panel.  If not, see <http://www.gnu.org/licenses/>.
#
# Author(s): Adonay Sanz Alsina <adonay@kademar.org>
# First develop date (of second version) 5 - feb - 2013
#
#


import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
from os import system
import platform
#import unicodedata
#from subprocess import getoutput
#from os import path
import resource
from bitnamiStackManager import bitnamiStackManager
import platform
from os import listdir
import dbus.mainloop.qt

class actionStack(QAction):
    def __init__(self, parent):
        QAction.__init__(self, parent)
        self.stack=""
        self.connect(self, SIGNAL("triggered()"), self.actionClickedFunction)

    def setStack(self,param):
        self.stack=param

    def actionClickedFunction(self):
        self.emit(SIGNAL("actClicked"), self.stack)        


class bitnamiController(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = uic.loadUi("bitnamiController.ui", self)
        #self.lampstackVersion="5.4.11-0"
        self.homeDir=QDir.homePath()
        self.bitnamiInstallationPath=self.homeDir+"/.lampstack"
        self.appDir=self.bitnamiInstallationPath+"/apps/"
        self.bitnamiControlScript=self.bitnamiInstallationPath+"/ctlscript.sh"
        self.autostartDir=self.homeDir+"/.config/autostart"
        self.cacheDir=self.homeDir+"/.cache/kademar-bitnami-controller/"
        self.movieIcon=QMovie(":/img/img/wait.gif")
        self.settings=QSettings(self.homeDir+"/.lampstack/kademar-bitnami-controller.ini",QSettings.IniFormat)
        self.appActions=[]
        self.appsMenu=QMenu(self.tr("Apps"))
        self.autostart=False
        self.settings=QSettings("Kademar","bitnamiController")


        
#############
####  TRAY MODULE & ACTIONS
#############
        #### TRAY ####
        self.tray = QSystemTrayIcon(self)
        self.trayMenu = QMenu()
     # Menu items
        self.action_start = QAction(QIcon(":/img/img/verd_p.png"), self.tr('Start Bitnami Server'), self)
        self.action_restart = QAction(QIcon(":/img/img/taronja_p.png"), self.tr('Restart Bitnami Server'), self)
        self.action_stop = QAction(QIcon(":/img/img/vermell_p.png"), self.tr('Stop Bitnami Server'), self)
        self.action_manage = QAction(QIcon(":/img/img/config.png"), self.tr('Manage Bitnami Stacks'), self)
        self.action_browse = QAction(QIcon(":/img/img/browse.png"), self.tr('Open Browser'), self)
        self.action_browseFile = QAction(QIcon(":/img/img/filemanager.png"), self.tr('FTP Apps'), self)
        self.action_exit = QAction(QIcon(":/img/img/exit.png"), self.tr('Exit Bitnami Control Panel'), self)

     # Append items to menu
        self.trayMenu.addAction(self.action_start)
        self.trayMenu.addAction(self.action_restart)
        self.trayMenu.addAction(self.action_stop)
        self.trayMenu.addSeparator()
        self.trayMenu.addAction(self.action_manage)
        self.trayMenu.addAction(self.action_browse)
        self.trayMenu.addAction(self.action_browseFile)
        self.trayMenu.addSeparator()
        self.trayMenu.addMenu(self.appsMenu)
        self.trayMenu.addSeparator()
        self.trayMenu.addAction(self.action_exit)

     # Tray icon definitions
        self.trayIcon = QIcon(":/img/img/bitnamistack.png")
        self.tray.setContextMenu(self.trayMenu)
        self.tray.setIcon(self.trayIcon)
        self.tray.setToolTip("Kademar Bitnami Control")
        self.tray.show()
#############
####  END  TRAY MODULE & ACTIONS
#############


#############
### NOTIFYCATION PART
#############
        try:
            dbus.mainloop.qt.DBusQtMainLoop(set_as_default=True)
            self.session_bus = dbus.SessionBus()
            self.obj =  self.session_bus.get_object("org.freedesktop.Notifications","/org/freedesktop/Notifications")
            self.interface = dbus.Interface(self.obj, "org.freedesktop.Notifications")
            self.notifySystem=True

        except Exception:
            self.interface = None
            self.notifySystem=False
            print(self.tr("unable to create DBUS connecton to notify"))
#############
### END NOTIFYCATION PART
#############

        ##Connectar Accions al fer click a un del menu, la function que executa
        self.connect(self.action_start, SIGNAL("triggered()"), self.startServer)
        self.connect(self.actionStart_Server, SIGNAL("triggered()"), self.startServer)
        
        self.connect(self.action_stop, SIGNAL("triggered()"), self.stopServer)
        self.connect(self.actionStop_Server, SIGNAL("triggered()"), self.stopServer)
     
        self.connect(self.action_restart, SIGNAL("triggered()"), self.restartServer)
        self.connect(self.actionRestart_Server, SIGNAL("triggered()"), self.restartServer)
        
        self.connect(self.action_manage, SIGNAL("triggered()"), self.openStackManager)
        self.connect(self.actionManage_Stacks, SIGNAL("triggered()"), self.openStackManager)
        
        self.connect(self.action_exit, SIGNAL("triggered()"), self.askForExit)
        self.connect(self.actionExit, SIGNAL("triggered()"), self.askForExit)

        self.connect(self.action_browse, SIGNAL("triggered()"), self.openBrowser)
        self.connect(self.actionOpen_Browser, SIGNAL("triggered()"), self.openBrowser)
        
        self.connect(self.actionOpen_Cache_Stack, SIGNAL("triggered()"), self.openCacheStack)

        self.connect(self.actionOpen_File_Manger, SIGNAL("triggered()"), self.openFileManager)
        self.connect(self.action_browseFile, SIGNAL("triggered()"), self.openFileManager)

        self.connect(self.actionBitnami_Documentation, SIGNAL("triggered()"), self.openBitnamiDocs)
        self.connect(self.actionApache_Documentation, SIGNAL("triggered()"), self.openApacheDocs)
        self.connect(self.actionComponents, SIGNAL("triggered()"), self.openBitnamiDocsComponent)
        self.connect(self.actionApps, SIGNAL("triggered()"), self.openBitnamiDocsApps)
        self.connect(self.actionMake_public_any_BitNami_Stack, SIGNAL("triggered()"), self.openBitnamiDocsPublic)
        self.connect(self.actionBitNami_LAMP_Stack_Readme, SIGNAL("triggered()"), self.openBitnamiDocsReadme)
        self.connect(self.actionMultiple_instances_of_the_same_App, SIGNAL("triggered()"), self.openBitnamiDocsMultiple)
        self.connect(self.actionBitNami_AMP_Stacks, SIGNAL("triggered()"), self.openBitnamiDocsAMP)
        self.connect(self.actionBitNami_Custom_PHP_application, SIGNAL("triggered()"), self.openBitnamiDocsCustomPHP)
        

        self.connect(self.actionAutostart_on_boot, SIGNAL("triggered()"), self.toggleAutostartOnBoot)
        self.connect(self.actionStart_on_tray, SIGNAL("triggered()"), self.toggleAutostartOnBoot)

        #Quan fas clic al tray executa eventsdeltray (function)
        self.tray.connect( self.tray, SIGNAL( "activated(QSystemTrayIcon::ActivationReason)" ), self.eventsdeltray )
        
        self.connect(self.ui.BStartServer, SIGNAL("clicked()"), self.startServer)
        self.connect(self.ui.BStopServer, SIGNAL("clicked()"), self.stopServer)
        self.connect(self.ui.BRestartServer, SIGNAL("clicked()"), self.restartServer)

        #Initial GUI State
        self.setChangingStatus()
        self.checkAutostart()
        
        self.prepareWatchFile()

        self.checkBitnamiInstallation()
        
        self.checkTrayStart()
        
    def toggleAutostartOnBoot(self):
        if QFile(self.autostartDir).exists():
            system("mkdir -p "+self.autostartDir)
        if self.autostart:
            #time to remove
            system("rm -f "+self.autostartDir+"/bitnami-controller.desktop")
            self.autostart=False
        else:
            #time to activate
            f=open(self.autostartDir+"/bitnami-controller.desktop",'w')
            f.writelines('[Desktop Entry]\n')
            f.writelines('Name=Bitnami Control Panel\n')
            f.writelines('Exec=bitnami-controller\n')
            f.writelines('Icon=/usr/share/bitnami-controller/bitnamistack.png\n')
            f.writelines('Terminal=false\n')
            f.writelines('Type=Application\n')
            f.writelines('Categories=Network;Internet\n')
            f.close()

            system("chmod +x "+self.autostartDir+"/bitnami-controller.desktop")
            self.autostart=True

        self.checkAutostart()
          
    def checkAutostart(self):
        if QFile(self.autostartDir+"/bitnami-controller.desktop").exists():
            state=""
            self.autostart=True
        else:
            state="no"
            self.autostart=False
        self.actionAutostart_on_boot.setIcon(QIcon(QPixmap(":/img/img/"+state+"tick.png")))
        
        
    def toggleAutostartOnBoot(self):
        #print(str(self.settings.value("startOnTray")).lower())
        if str(self.settings.value("startOnTray")).lower() == "true":
            self.settings.setValue("startOnTray",False)
        else:
            self.settings.setValue("startOnTray",True)
        self.checkTrayStart()
	  
	  
    def checkTrayStart(self):
        if str(self.settings.value("startOnTray")).lower() == "true":
            state=""
            self.autostart=True
        else:
            state="no"
            self.autostart=False
        self.actionStart_on_tray.setIcon(QIcon(QPixmap(":/img/img/"+state+"tick.png")))
        
        
    def openBitnamiDocs(self):
        self.apa = QProcess()
        self.apa.start("xdg-open http://wiki.bitnami.org/")
    def openApacheDocs(self):
        self.apa = QProcess()
        self.apa.start("xdg-open http://wiki.bitnami.org/Components/Apache")
    def openBitnamiDocsComponent(self):
        self.apa = QProcess()
        self.apa.start("xdg-open http://wiki.bitnami.org/Components")
    def openBitnamiDocsApps(self):
        self.apa = QProcess()
        self.apa.start("xdg-open http://wiki.bitnami.org/Applications")
    def openBitnamiDocsPublic(self):
        self.apa = QProcess()
        self.apa.start("xdg-open http://wiki.bitnami.org/Native_Installers_Quick_Start_Guide#How_to_install_and_make_public_any_BitNami_Stack.3f")
    def openBitnamiDocsReadme(self):
        self.apa = QProcess()
        self.apa.start("xdg-open "+self.bitnamiInstallationPath+"/README.txt")
    def openBitnamiDocsMultiple(self):
        self.apa = QProcess()
        self.apa.start("xdg-open http://answers.bitnami.org/questions/7948/installing-second-wordpress-stack-on-same-ec2-server")
    def openBitnamiDocsCustomPHP(self):
        self.apa = QProcess()
        self.apa.start("xdg-open http://wiki.bitnami.org/Applications/BitNami_Custom_PHP_application")
    def openBitnamiDocsAMP(self):
        self.apa = QProcess()
        self.apa.start("xdg-open http://wiki.bitnami.org/Infrastructure_Stacks/BitNami_AMP_Stacks")
        

    def openCacheStack(self):
        self.apa = QProcess()
        self.apa.start("xdg-open "+self.cacheDir)

        
    def checkBitnamiInstallation(self):
        if not QFile(self.bitnamiControlScript).exists():
            if platform.architecture()[0] == "64bit":
                arch="-x64"
                grepParam="-i"
            else:
                #arch="i686"
                arch=""
                grepParam="-v"
            #print("Should install lampstack")
            app.processEvents()

	      #check system cache
            if not QFile("cache/bitnami-lampstack-linux"+arch+"-installer.run").exists():
	      #time to check home
                if not QFile(self.cacheDir+"/bitnami-lampstack-linux"+arch+"-installer.run").exists():
                   #not found, time to download
                    if not QFile(self.cacheDir).exists():
                       #cache folder not exists, create it
                        system("mkdir -p "+self.cacheDir)
                    #donwload stack
                    self.sendNotify(self.tr("Downloading Bitnami Server"), self.tr("No bitnami servers where found. Now is downloading the new version, please wait."))
                    #system("""download=$(for i in  `wget -O- http://bitnami.org/stack/lamp | grep -i download_file_link | grep -i linux | grep -v module | grep """+grepParam+""" x64 | cut -d\\" -f2 `; do echo $i; break; done) ; wget $download -O """+self.cacheDir+"""/bitnami-lampstack-linux"""+arch+"""-installer.run ; chmod +x """+self.cacheDir+"""/bitnami-lampstack-linux"""+arch+"""-installer.run""")
                    system("""download=$(wget http://bitnami.com/stack/lamp/installer -O- | grep -i "a href" | grep -i linux"""+arch+"""-installer.run | grep -i direct_download_link | grep -v 'role="button"' | while read i;  do echo $i | cut -d\\" -f2; break; done)  ; wget http://www.bitnami.com/$download?with_popup_skip_signin=1 -O """+self.cacheDir+"""/bitnami-lampstack-linux"""+arch+"""-installer.run ; chmod +x """+self.cacheDir+"""/bitnami-lampstack-linux"""+arch+"""-installer.run""")

                    installer=self.cacheDir+"/bitnami-lampstack-linux"+arch+"-installer.run"
                else:
                   #founded on home
                   installer=self.cacheDir+"/bitnami-lampstack-linux"+arch+"-installer.run"
            else:
               #found system cache
                installer="cache/bitnami-lampstack-linux"+arch+"-installer.run"
            
            self.sendNotify(self.tr("Installing Bitnami Server"), self.tr("The bitnami server is installing, please wait during the process"))
            system(installer+" --unattendedmodeui minimal --mysql_password kademar --prefix "+self.bitnamiInstallationPath+" --launchbch 0 --mode unattended --mysql_port 3307 --base_password kademar --installer-language es")

        self.setChangingStatus()
        self.startServer()
        self.reloadAppMenu()
            
    def openFileManager(self):
        self.fm=QProcess()
        self.fm.start('xdg-open "'+self.bitnamiInstallationPath+'/apps"')

    def checkExecutionStatus(self):
        
        ret=self.execShellProcess("bash", "-c", self.bitnamiControlScript+" status | grep -i already")
        ret=ret.replace("'","").replace("b","")
        #print(ret)
        if ret != "":
            #already Started
            status=1
            self.ui.LStatus.setText(self.tr("Started"))
            self.iStatus.setPixmap(QPixmap(":/img/img/verd_p.png"))
            self.sendNotify(self.tr("Bitnami Server Started"), self.tr("The server now is started and fully working"))
        else:
            #Not Started
            status=0
            self.ui.LStatus.setText(self.tr("Stopped"))
            self.sendNotify(self.tr("Bitnami Server Stopped"), self.tr("The server now is stopped"))
            self.iStatus.setPixmap(QPixmap(":/img/img/vermell_p.png"))

        for i in [ self.actionRestart_Server, self.action_restart, self.ui.BRestartServer,self.ui.BStartServer, self.ui.BStopServer, self.action_start, self.actionStart_Server, self.action_stop, self.actionStop_Server, self.action_browse, self.actionOpen_Browser, self.action_manage, self.actionManage_Stacks ]:
            i.setEnabled(1)
        self.actionRestart_Server.setEnabled(1)
        self.action_restart.setEnabled(1)
        self.ui.BRestartServer.setVisible(1)
        self.ui.BStartServer.setVisible(not status)
        self.ui.BStopServer.setVisible(status)
        self.action_start.setVisible(not status)
        self.actionStart_Server.setVisible(not status)
        self.action_stop.setVisible(status)
        self.actionStop_Server.setVisible(status)
        self.action_browse.setEnabled(status)
        self.actionOpen_Browser.setEnabled(status)
        self.action_manage.setEnabled(status)
        self.actionManage_Stacks.setEnabled(status)
        self.ui.menuApps.setEnabled(status)
        self.appsMenu.setEnabled(status)
        self.movieIcon.stop()

    def reloadAppMenu(self):
        #print("reloading")
        listDir=listdir(self.appDir)
        self.ui.menuApps.clear()
        self.appsMenu.clear()
        
        for filename in sorted(listDir):
            if filename != "" and filename != "heroku":
                self.appActions.append(actionStack(self))
                actual=len(self.appActions)-1
                self.appActions[actual].setText(filename)
                self.ui.menuApps.addAction(self.appActions[actual])
                self.appsMenu.addAction(self.appActions[actual])
                imgPath=":/img/img/stacks/"+filename+".png"
                if not QFile(imgPath).exists():
                    #print("not exists "+imgPath)
                    imgPath=self.cacheDir+filename+".png"
                self.appActions[actual].setIcon(QIcon(QPixmap(imgPath)))
                self.appActions[actual].setStack(filename)
                self.connect(self.appActions[actual], SIGNAL("actClicked"), self.openBrowser)
                
                
    def setChangingStatus(self):
        for i in [ self.appsMenu, self.ui.menuApps, self.actionRestart_Server, self.action_restart, self.ui.BRestartServer,self.ui.BStartServer, self.ui.BStopServer, self.action_start, self.actionStart_Server, self.action_stop, self.actionStop_Server, self.action_browse, self.actionOpen_Browser, self.action_manage, self.actionManage_Stacks ]:
            i.setEnabled(0)
        
        self.movieIcon.start()
        self.ui.iStatus.setMovie(self.movieIcon)
        self.LStatus.setText("")
        
    def startServer(self):
        self.setChangingStatus()
        self.start=QProcess()
        #self.connect(self.actionOpen_Browser, SIGNAL("triggered()"), self.openBrowser)
        self.connect(self.start, SIGNAL("finished(int)"), self.checkExecutionStatus)
        self.start.start(self.bitnamiControlScript+" start")

    def restartServer(self):
        self.setChangingStatus()
        self.restart=QProcess()
        #self.connect(self.actionOpen_Browser, SIGNAL("triggered()"), self.openBrowser)
        self.connect(self.restart, SIGNAL("finished(int)"), self.checkExecutionStatus)
        self.restart.start(self.bitnamiControlScript+" restart")

    def stopServer(self):
        self.setChangingStatus()
        app.processEvents()
        
        #Only for status icon on initial execution
        self.stop=QProcess()
        #self.connect(self.actionOpen_Browser, SIGNAL("triggered()"), self.openBrowser)
        self.connect(self.stop, SIGNAL("finished(int)"), self.checkExecutionStatus)
        self.stop.start(self.bitnamiControlScript+" stop")
        
        #system(self.bitnamiControlScript+" stop")
        #self.checkExecutionStatus()

    def openStackManager(self):
        self.manager=bitnamiStackManager()
        self.manager.show()
        self.connect(self.manager, SIGNAL("reload"), self.reloadAppMenu)
        

    def openBrowser(self, param=None):
        self.pro = QProcess()
        if param:
            self.pro.start("xdg-open http://localhost:8080/"+param)
        else:
            self.pro.start("xdg-open http://localhost:8080")

#Set visible/invisible main window
    def mainwindow(self):
        widget.setVisible( not widget.isVisible() )

#Click events on tray icon
    def eventsdeltray(self, arEvent):
       #Left button click
       if arEvent == self.tray.Trigger:
          self.mainwindow()

#Close event of window
    def closeEvent(self, event):
        event.ignore()
        self.mainwindow()

#Ask for a real exit of App
    def askForExit(self):
        preg = QMessageBox.critical(self, self.tr("Exit from Kademar Bitnami Control Panel"), self.tr("Do you want to exit from Kademar Bitnami Control Panel and Stop the Bitnami Server?"), QMessageBox.Yes| QMessageBox.No,  QMessageBox.No)
        if preg == QMessageBox.Yes:
            self.stopServer()
            app.processEvents()
            self.stop.waitForFinished()
            app.quit()

    def execShellProcess(self, idCommand, idParam = "", idParam2 = ""):
        #Execute a shell order and return the result
        # for pipe commands use idCommand="/bin/bash" idParam="-c" idParam2="shell | piped command"
        param=[]
        if idParam:
            param.append(idParam)
        if idParam2:
            param.append(idParam2)
        proc = QProcess()
        proc.start(idCommand, param)
        proc.waitForFinished()
        result = proc.readAll()
        #self.logMessage(str(result))
        proc.close()
        return str(result)
     
     
    def prepareWatchFile(self):
        self.fileWatcher=QFileSystemWatcher()
        self.fileWatcher.addPath("/usr/share/bitnami-controller/bitnamiController.py")
        self.connect(self.fileWatcher, SIGNAL("fileChanged(const QString&)"), self.fileChangedSlot)

    def fileChangedSlot(self):
        self.sendNotify(self.tr("Bitnami Control Updated"),self.tr("It has been updated, you should reboot the Kademar Bitnami Control Panel to get the new features."))
        self.fileWatcher.blockSignals(True)
 
     
    def sendNotify(self, title, body):
        if self.notifySystem:
            self.app_name="Kademar Bitnami Control"
            #self.summary="Starting Server"
            #self.body="sdf"
            self.app_icon="/usr/share/bitnami-controller/bitnamistack.png"
            self.expire_timeout=5000
            self.actions = [] #["update", "\nUpdate\n"]
            self.hints = {}
            self.interface.Notify(self.app_name, 0, self.app_icon, title, body, self.actions, self.hints, self.expire_timeout)

if len(sys.argv)<=1:
    pass
   #If the first argument is NOT session (kde autostart) execute it
elif not sys.argv[1]=="-session":
    pass
else:  #STOP
    print("Not starting, it's a KDE session autoload")
    sys.exit()

app = QApplication(sys.argv)
locale = QLocale.system().name()
qtTranslator = QTranslator()
if qtTranslator.load("tr/"+locale.split("_")[0]+".qm"):
    app.installTranslator(qtTranslator)
    print ("Loaded "+locale)
elif qtTranslator.load("tr/en.qm"):
    app.installTranslator(qtTranslator)
    print ("Loaded "+locale)

widget = bitnamiController()

settings=QSettings("Kademar","bitnamiController")
if str(settings.value("startOnTray")).lower() != "true":
    widget.show()
    #print("show")

#else:
    #print("not show")
#print(settings.value("startOnTray"))

app.exec_()

