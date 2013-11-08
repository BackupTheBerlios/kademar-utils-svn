#!/usr/bin/python

#
# Kademar Bitnami Controller
# 5 - feb - 2013
# License GNU/GPL 3 or higher
# Adonay Sanz Alsina <adonay@kademar.org>
#

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
from os import system, path
import platform
#import unicodedata
#from subprocess import getoutput
from os import listdir
import resource
from socket import socket, AF_INET, SOCK_STREAM

class bitnamiStackManager(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = uic.loadUi("bitnamiStackManager.ui", self)
        #self.movieIcon=QMovie(":/img/img/wait.gif")
        self.homeDir=QDir.homePath()
        self.appDir=self.homeDir+"/.lampstack/apps/"
        self.cacheDir=self.homeDir+"/.cache/kademar-bitnami-controller/"
        system("mkdir -p '"+self.cacheDir+"'")
        self.connect(self.ui.BBack, SIGNAL("clicked()"), self.backButton)
        self.installing=0
        self.settings=QSettings(self.homeDir+"/.lampstack/kademar-bitnami-controller.ini",QSettings.IniFormat)
        
        #self.movieIcon.start()
        self.movieIcon=QMovie(":/img/img/wait.gif")
        self.ui.iDownloading.setMovie(self.movieIcon)
        

        self.checkInternetConnection() #check if we can install new stacks or not
        self.checkBitnamiStacks()
        
        
    def backButton(self):
        if self.installing:
            self.checkBitnamiStacks()
        else:
            self.close()
        
    def checkBitnamiStacks(self):
        #self.ui.frame.setVisible(0)
        self.installing=0
        self.ui.stackedWidget.setCurrentWidget(self.ui.stacksPage) #put the page
        
        
        #prepare table
        table = self.ui.tableWidget
        table.clear()
        table.setRowCount(0)

        table.verticalHeader().setVisible(False)
        table.horizontalHeader().hide()
        
        table.setColumnCount(4)
        value=int(str(int((self.ui.width()-120)/9)).split(".")[0])
        table.horizontalHeader().resizeSection(0, 70)#image
        table.horizontalHeader().resizeSection(1, value*4) #name
        table.horizontalHeader().resizeSection(2, value*2) #version
        table.horizontalHeader().resizeSection(3, value*3) #button

        table.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding);

        #read the stack folder
        listDir=listdir(self.appDir)
        
        #create a icon for each stack on appDir
        for filename in sorted(listDir):
            if filename != "" and filename != "heroku":
                #Create a new row                
                table.setRowCount(table.rowCount()+1)
                self.actualRow=table.rowCount()-1
                
                #define the stack icon
                # on the resource
                # hack for some icon names that change from real folder
                if filename == "tinytinyrss":
                    afilename = "tiny-tiny-rss"
                #elif filename == "phpBB3":
                    #afilename = "phpbb"
                else:
                    afilename = filename
                imgPath=":/img/img/stacks/"+afilename+".png"
                if not QFile(imgPath).exists():
                    #if not, go to cache dir
                    imgPath=self.cacheDir+filename+".png"
                    
                #put the iocn on the table
                myPixmap = QPixmap(imgPath)
                myScaledPixmap = myPixmap.scaled(QSize(70,70), Qt.KeepAspectRatio)
                ##self.label.setPixmap(myScaledPixmap)
                img = QLabel(table)
                img.setPixmap(myScaledPixmap)
                table.setCellWidget(self.actualRow, 0, img)
            
                #Set the label
                label=QLabel()
                if filename == "tinytinyrss":
                    filename = "Tiny-Tiny-RSS"
                else:
                    afilename=filename
                label.setText("<font color='Blue'><b>"+afilename.capitalize()+"</b></font>")
                label.setAlignment(Qt.AlignCenter)
                table.setCellWidget(self.actualRow,1, label)

                #Get the version 
                version=""
                if filename == "phpmyadmin":
                    #Get from the readme
                    version=self.execShellProcess("bash", "-c", "grep Version "+self.appDir+"/phpmyadmin/htdocs/README | awk ' { print $2 } '").replace("b","").replace("'","").replace("\\n","")
                else:
                    #if isn't phpmyadmin, read from ower config file
                    version=self.settings.value(filename, version)

                #Write version label            
                label=QLabel()
                label.setText("<font color='Blue'>"+version+"</font>")
                label.setAlignment(Qt.AlignCenter)
                table.setCellWidget(self.actualRow,2, label)

                #If we can uninstall, create the icon
                if QFile(self.appDir+"/"+filename+"/"+"uninstall").exists():
                    btn = buttonForStacks(table)
                    btn.setIcon(QIcon(QPixmap(":/img/img/uninstall.png")))
                    btn.setIconSize(QSize(40,40))
                    btn.setText(self.tr("Uninstall"))
                    btn.setAction("uninstall")
                    btn.setStack(filename)
                    table.setCellWidget(self.actualRow, 3, btn)
                    self.connect(btn, SIGNAL("btnClicked"), self.doActionForStack)
                
                #Change Row height
                table.verticalHeader().resizeSection(self.actualRow, 75) #name
        
        if self.internet:
            #Read available stacks from the internet        
            bitnamiStacks=self.execShellProcess("bash","-c","""wget http://bitnami.com/stack/lamp/modules -O- | grep -i png | grep -i "/stack/" """).replace("b'","").replace("'","")
            #print (listDir)
            for i in sorted(bitnamiStacks.split("\\n")):
                if i != "":
                    line=i.split('"')
                    #print(line)   #['                    <a href=', '/stack/sugarcrm', '><img alt=', 'SugarCRM', ' src=', '//d33np9n32j53g7.cloudfront.net/assets/stacks/sugarcrm/img/sugarcrm-stack-110x117-5e9742a1bd64ef6360301980785c3e0e.png', ' /></a>']
                    url=line[1]
                    name=line[3]
                    shortName=url.split("/")[2]
                    #print (shortName)
                    icon="http:"+line[5]
                #download all icons
                #system("wget "+icon+" -O cache/"+url.split("/")[2]+".png")

                    #Put available to download on manager if isn't installed
                    # let's hack the system to find cms that differs from shortname to install folder name
                    if shortName == "tiny-tiny-rss":
                        shortName = "tinytinyrss"
                    elif shortName == "phpbb":
                        shortName = "phpBB3"
                    elif shortName == "tiki-wiki-cms-groupware":
                        shortName = "tiki"

                    #if not find, show button to install
                    if not shortName in listDir:
                        table.setRowCount(table.rowCount()+1)
                        self.actualRow=table.rowCount()-1

                        imgPath=":/img/img/stacks/"+shortName+".png"
                        if not QFile(imgPath).exists():
                            #print("not exists "+imgPath)
                            imgPath=self.cacheDir+shortName+".png"
                            if not QFile(imgPath).exists():
                                #print("not exists "+imgPath)
                                system("wget "+icon+" -O "+self.cacheDir+shortName+".png")
                        myPixmap = QPixmap(imgPath)
                        myScaledPixmap = myPixmap.scaled(QSize(70,70), Qt.KeepAspectRatio)
                        ##self.label.setPixmap(myScaledPixmap)
                        img = QLabel(table)
                        img.setPixmap(myScaledPixmap)
                        table.setCellWidget(self.actualRow, 0, img)
                
                        #Set name cms - not installed label in grey 
                        label=QLabel()
                        label.setText("<font color='Grey'>"+name.capitalize()+"</font>")
                        label.setAlignment(Qt.AlignCenter)
                        #table.setItem(0,1,QTableWidgetItem(filename))
                        table.setCellWidget(self.actualRow,1, label)
                    
                        #Set not installed label in grey 
                        label=QLabel()
                        label.setText("<font color='Grey'>"+self.tr("Not Installed")+"</font>")
                        label.setAlignment(Qt.AlignCenter)
                        table.setCellWidget(self.actualRow,2, label)
                
                
                        btn = buttonForStacks(table)
                        btn.setIcon(QIcon(QPixmap(":/img/img/next.png")))
                        btn.setIconSize(QSize(40,40))
                        btn.setAction("versions")
                        btn.setStack(shortName)
                        btn.setText(self.tr("Check versions"))
                        self.connect(btn, SIGNAL("btnClicked"), self.doActionForStack)
                        table.setCellWidget(self.actualRow, 3, btn)
        
                        table.verticalHeader().resizeSection(self.actualRow, 80) #name
                        #table.setRowCount(table.rowCount()-1)
        else:
            QMessageBox.critical(self, self.tr("Not internet connection"), self.tr("You need a internet connection to be able to install new stacks"), QMessageBox.Ok)

                    
    def doActionForStack(self, stack, action,url,version):
        if stack == "tiki-wiki-cms-groupware":
            stack="tiki"
        elif stack == "tiny-tiny-rss":
            stack="tinytinyrss"
        #print(action, stack)
        if action=="uninstall":
            ans = QMessageBox.critical(self, self.tr("Uninstall of")+" "+stack, self.tr("Are you sure to uninstall this stack?"), QMessageBox.Yes| QMessageBox.No,  QMessageBox.No)
            if ans == QMessageBox.Yes:
                options=self.setOptionsUninstall(stack)
                system(self.appDir+stack+"/uninstall --installer-language "+options+" --mode unattended  --unattendedmodeui minimal")
                self.checkBitnamiStacks()
            
        elif action=="versions":
            self.installing=1
            #self.ui.frame.setVisible(1)
            table = self.ui.tableWidget
            table.setRowCount(0)
            table.clear()
            
            if platform.architecture()[0] == "64bit":
                arch="x64-"
            else:
                #arch="i686"
                arch=""
            
            print("""wget -O- http://bitnami.org/stack/lamp/modules | grep -i """+stack+""" | grep -i direct_download_link | grep -i run | grep -i "a href" | grep -i linux-"""+arch+"""installer | grep -i '\.run' | grep -i 'role="button"' """)
            bitnamiStacks=self.execShellProcess("bash","-c","""wget -O- http://bitnami.org/stack/lamp/modules | grep -i """+stack+""" | grep -i direct_download_link | grep -i run | grep -i "a href" | grep -i linux-"""+arch+"""installer | grep -i '\.run' | grep -i 'role="button"' """).replace("b'","").replace("'","")
            #print(hola.split("\\n"))
            for i in bitnamiStacks.split("\\n"):
                if i != "":
                    line=i.split('"')
                    #print(line) 
                    #['<a href=', '/redirect/to/19336/bitnami-wordpress-3.5.1-2-module-linux-x64-installer.run', ' role=', 'button', ' data-target=', '#downloadFileModal-19336', ' style=', 'outline: none; display: none !important', ' class=', 'indirect_download_link ', ' data-toggle=', 'modal', '><img alt=', 'Download', ' src=', '//d33np9n32j53g7.cloudfront.net/assets/downloads-button-bc25419be1f20ee88e835c543da41511.png', ' /></a>']
                    
                    url="http://www.bitnami.com"+line[1]

                    version=line[1].split("/")[4].split("-")[2]

                    table.setRowCount(table.rowCount()+1)
                    self.actualRow=table.rowCount()-1

                    imgPath=":/img/img/stacks/"+stack+".png"
                    if not QFile(imgPath).exists():
                        ##print("not exists "+imgPath)
                        imgPath=self.cacheDir+stack+".png"
                        #if not QFile(imgPath).exists():
                            #print("not exists "+imgPath)
                            #system("wget "+icon+" -O "+self.cacheDir+shortName+".png")
                    myPixmap = QPixmap(imgPath)
                    myScaledPixmap = myPixmap.scaled(QSize(70,70), Qt.KeepAspectRatio)
                    ##self.label.setPixmap(myScaledPixmap)
                    img = QLabel(table)
                    img.setPixmap(myScaledPixmap)
                    table.setCellWidget(self.actualRow, 0, img)
                
                    label=QLabel()
                    label.setText("<font color='Grey'>"+stack.capitalize()+"</font>")
                    label.setAlignment(Qt.AlignCenter)
                    ##table.setItem(0,1,QTableWidgetItem(filename))
                    table.setCellWidget(self.actualRow,1, label)
                    
                    label=QLabel()
                    label.setText("<font color='Grey'>"+version+"</font>")
                    label.setAlignment(Qt.AlignCenter)
                    table.setCellWidget(self.actualRow,2, label)
                
                    btn = buttonForStacks(table)
                    btn.setIcon(QIcon(QPixmap(":/img/img/download.png")))
                    btn.setIconSize(QSize(40,40))
                    btn.setAction("install")
                    btn.setStack(stack)
                    btn.setUrl(url)
                    btn.setVersion(version)
                    
                    filename=path.basename(url)
                    
                    if QFile("cache/"+filename).exists() or not QFile(self.cacheDir+filename).exists():
                        btn.setText(self.tr("Download and Install"))
                    else:
                        btn.setText(self.tr("Install"))
                    
                    self.connect(btn, SIGNAL("btnClicked"), self.doActionForStack)
                    table.setCellWidget(self.actualRow, 3, btn)
        
                    table.verticalHeader().resizeSection(self.actualRow, 70) #name
        elif action == "install": 
       #Install some version
            #print("Installing", stack, url)
            options=self.setOptionsInstall(stack)
                
            filename=path.basename(url)
            if not QFile("cache/"+filename).exists():  #Official cache in /usr/share/bitnami
                if not QFile(self.cacheDir+filename).exists(): #Download
                    #print("do not exists, downloading")
                    self.movieIcon.start()
                    self.ui.stackedWidget.setCurrentWidget(self.ui.downloadPage)
                    self.ui.LUrl.setText(url)
                    self.pro=QProcess()
                    
                    self.pro.start("wget "+url+"?with_popup_skip_signin=1 -O "+self.cacheDir+filename)
                    #self.pro.waitForFinished()
                    
                    self.connect(self.pro, SIGNAL("finished(int)"), self.installStack)

                    #a=QWidget(None)
                    #a.show()
                else:  #Install from official (root) cache
                    #print("installing from "+self.cacheDir+filename)
                    system(self.cacheDir+filename+" --unattendedmodeui minimal  --prefix "+self.homeDir+"/.lampstack --mode unattended --base_user admin --base_password kademar --installer-language "+options)
                    #line2=line[1].split("/") #'bitnami-redmine-1.4.7-1-module-linux-x64-installer.run'
                    self.settings.value(stack, version)
                    
                    
                    self.checkBitnamiStacks()
            else: #install from Home cache
                #system("chmod +x '"+self.cacheDir+filename+"'")
                #print("installing from cache/"+filename)
                system("cache/"+filename+" --unattendedmodeui minimal  --prefix "+self.homeDir+"/.lampstack--mode unattended  --base_user admin --base_password kademar --installer-language "+options)
                self.settings.value(stack, version)
                self.checkBitnamiStacks()
            
    def installStack(self):
        filename=path.basename(self.ui.LUrl.text())
        options=self.setOptionsInstall(filename)

        system("chmod +x '"+self.cacheDir+filename+"'")
        system(self.cacheDir+filename+" --unattendedmodeui minimal  --prefix "+self.homeDir+"/.lampstack --mode unattended  --base_user admin --base_password kademar --installer-language "+options)
        self.checkBitnamiStacks()


    def checkInternetConnection(self):
        self.internet=0
        testConn=socket(AF_INET,SOCK_STREAM)
        try:
            testConn.connect(('www.bitnami.org',80))
            testConn.close()
            self.internet=1
        except:
            testConn.close()
            self.internet=0

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

    def closeEvent(self, event):
        self.emit(SIGNAL("reload"))
        event.accept()
        
    def setOptionsInstall(self, stack):
        options="es --launchbch 0"
        if "magento" in stack:
            options="es --launchbch 0 --magento_admin_pass kademar"
        elif "ezpublish" in stack:
                options="en --launchbch 0"
        elif "thinkup" in stack:
                options="es --launchbch 0 --thinkup_admin_password kademar"
        elif "postgresql" in stack:
                options="es --postgres_password kademar"

        return options

    def setOptionsUninstall(self, stack):
        options="es"
        if  "ezpublish" in stack:
                options="en"

        return options

class buttonForStacks(QPushButton):
    def __init__(self, parent=None):
        QPushButton.__init__(self)
        self.stackName=""
        self.action=""
        self.url=""
        self.version=""
        self.connect(self, SIGNAL("clicked()"), self.buttonClickedFunction)

    def setStack(self, param):
        self.stackName=param

    def setAction(self, param):    
        self.action=param

    def setUrl(self, param):
        self.url=param

    def setVersion(self,param):
        self.version=param

    def buttonClickedFunction(self):
        self.emit(SIGNAL("btnClicked"), self.stackName, self.action, self.url, self.version)
    
        

#apps = QApplication(sys.argv)
#widget = bitnamiStackManager()
#widget.show()
#app.exec_()


