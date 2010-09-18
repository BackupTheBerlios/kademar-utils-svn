#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

#from commands import getoutput
from os import path, system, walk, symlink, rename

#import funcions_k

from ui_audioconversor import Ui_FormAudioConversor as Ui_Form

global nomore, globalpath
nomore=False

class AudioConversor(QWidget):
    def __init__(self, parent=None):
        global tmpfile, fileformats, globalpath

        QWidget.__init__(self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setAcceptDrops(1)


        tmpfile="/tmp/audioconversor-tmp-file"
        globalpath="/usr/share/kademar/utils/audioconversor/"
        self.directoryIcon=globalpath+"img/folder.png"
        self.soundIcon=globalpath+"img/sound.png"
        self.processIcon=globalpath+"img/gear.png"
        self.process2Icon=globalpath+"img/gear2.png"
        self.inoredIcon=globalpath+"img/ignored.png"
        self.inoredIconTarget=globalpath+"img/ignored_target.png"
        self.stopedIcon=globalpath+"img/stoped.png"
        self.okIcon=globalpath+"img/ok.png"
        fileformats=" *.mp3 *.ogg *.wma *.wav *.flv .mid *.midi *.pcm *.umx *.kar *.spc *.psf *.ra *.ape *.flac *.mpc *.flc *.avi *.mkv *.mp4)"
        self.ui.listWidget.setIconSize(QSize(32,32))

        self.ui.pages.setCurrentIndex(0)

        self.ui.horizontalSlider.setVisible(0)
        self.ui.l_num_bitrate.setVisible(0)
        self.ui.lineEdit.setText(QDir.homePath()+"/audioconversor")

#####  SIGNAL & SLOTS  #####
        self.connect(self.ui.b_sortir, SIGNAL("clicked()"), self.boto_sortir)
        self.connect(self.ui.b_sortir_2, SIGNAL("clicked()"), self.boto_sortir)

        #self.connect(self.ui.b_convertaudio, SIGNAL("clicked()"), self.boto_conversor)
        self.connect(self.ui.b_addFolder, SIGNAL("clicked()"), self.boto_addFolder)
        self.connect(self.ui.b_clearList, SIGNAL("clicked()"), self.boto_clearList)
        self.connect(self.ui.b_addFile, SIGNAL("clicked()"), self.boto_addFile)
        self.connect(self.ui.b_removeFile, SIGNAL("clicked()"), self.boto_removeFile)
        self.connect(self.ui.b_chooseFormat, SIGNAL("clicked()"), self.boto_chooseFormat)
        self.connect(self.ui.cb_format, SIGNAL("currentIndexChanged (int)"), self.combobox_format)
        self.connect(self.ui.b_browse, SIGNAL("clicked()"), self.boto_browse)
        self.connect(self.ui.b_back, SIGNAL("clicked()"), self.boto_back)
        self.connect(self.ui.b_final, SIGNAL("clicked()"), self.final)
        self.connect(self.ui.horizontalSlider, SIGNAL("sliderMoved (int)"), self.newValueOGG)
        self.connect(self.ui.b_stop, SIGNAL("clicked()"), self.stop)
        self.connect(self.ui.b_back_2, SIGNAL("clicked()"), self.boto_b_back_2)

#### END SIGNAL & SLOTS ####

    def newValueOGG(self, num):
        self.ui.l_num_bitrate.setText(QString(num))

    def boto_back(self):
        self.ui.pages.setCurrentIndex(0)
        for i in [ self.ui.b_addFile, self.ui.b_addFolder, self.ui.b_clearList, self.ui.b_removeFile]:
            i.setEnabled(1)

    def combobox_format(self, num):
        if num==0:  #MP3
            self.ui.l_bitrate.setVisible(1)
            self.ui.cb_bitrate.setVisible(1)
            self.ui.horizontalSlider.setVisible(0)
            self.ui.l_num_bitrate.setVisible(0)
        elif num==1:  #OGG
            self.ui.cb_bitrate.setVisible(0)
            self.ui.horizontalSlider.setVisible(1)
            self.ui.l_bitrate.setVisible(1)
            self.ui.l_num_bitrate.setVisible(1)
        elif num==2:  #WAV
            self.ui.horizontalSlider.setVisible(0)
            self.ui.l_bitrate.setVisible(0)
            self.ui.cb_bitrate.setVisible(0)
            self.ui.l_num_bitrate.setVisible(0)

    def boto_conversor(self):
        self.ui.pages.setCurrentIndex(0)
        self.ui.b_convertaudio.setVisible(0)

    def boto_sortir(self):
        self.close()

    def boto_browse(self):
        directory = QFileDialog.getExistingDirectory(self, self.tr("Enter the directory to put converted files inside"), QDir.homePath())
        #print directory
        if len(directory)>0:
            self.ui.lineEdit.setText(directory)

    def boto_addFolder(self, directory=None, parent=None):
        global fileformats
        if not parent:
            directory = QFileDialog.getExistingDirectory(self, self.tr("Search for directory to add"), QDir.homePath())
            directory=[directory]
        #print directory
        if len(directory)>0:
            for d in directory:
                if QMessageBox.critical(self, self.tr("Recursive Add?"), self.tr("Do you want to add Sound files inside folder")+" "+d+" "+self.tr("recursivelly?") , QMessageBox.No, QMessageBox.Ok) == QMessageBox.Ok:
                    recursiu=True
                else:
                    recursiu=False

                self.llista=[]

                contador=0
                #print d
                todos = walk(str(d))
                for path, dirnames, filenames in todos:
                    contador+=1
                    for i in filenames:
                        if str(fileformats).find(i[-3:].lower())<>-1:  #if it's a recognized audio file put it
                            self.llista.append(path+'/'+i)
                    if not recursiu:
                        if contador==1:
                            break
                self.boto_addFile(self.llista, "parent")  # add file by file

    def boto_addFile(self, files=None, parent=None):
        if not parent:
            files = QFileDialog.getOpenFileNames(self, self.tr("Search for one or more files to add"),QDir.homePath(), self.tr("Sound")+fileformats)

        for o in files:
            if o:
                a=QListWidgetItem(self.ui.listWidget)
                a.setText(o)
                a.setIcon(QIcon(self.soundIcon))
                self.ui.listWidget.addItem(a)

    def boto_removeFile(self):
        for i in self.ui.listWidget.selectedItems():
            row=self.ui.listWidget.row(i)
            self.ui.listWidget.takeItem(row)

    def boto_clearList(self):
        if self.ui.listWidget.count()>0:
            if QMessageBox.critical(self, self.tr("Empty List"), self.tr("Are you sure to clear actual convert list?"), QMessageBox.No, QMessageBox.Ok) == QMessageBox.Ok:
                self.ui.listWidget.clear()

    #def filterFile(self, file):

    def dropEvent(self, event):
        file=str(event.mimeData().text().toLocal8Bit())
        returned=file.replace("file://","").split("\n")

        work_files=[]
        work_folders=[]

        for item in returned:
            if not path.isdir(item):

                if str(fileformats).find(item[-3:].lower())<>-1:  #if it's a recognized audio file put it
                    work_files.append(item)
            else:
                work_folders.append(item)

        self.boto_addFile(work_files, "parent")
        self.boto_addFolder(work_folders, "parent")


    def dragEnterEvent(self, event):
        """
        allow drag and drop actions
        """
        if event.mimeData().hasText():
            event.accept()

    def boto_chooseFormat(self):
        if self.ui.listWidget.count()>0:
            self.ui.pages.setCurrentIndex(1)
            for i in [ self.ui.b_addFile, self.ui.b_addFolder, self.ui.b_clearList, self.ui.b_removeFile]:
                i.setEnabled(0)
        else:
            QMessageBox.critical(self, self.tr("Sound Files"), self.tr("At least, you need to add a file to convert it.")) , QMessageBox.No 


    def final(self):
        global item, file, format, mp3bitrate, oggbitrate, folder, formats
        formats=[ "mp3", "ogg", "wav" ]
        process=True
        self.ui.pages.setCurrentIndex(2)
        folder=self.ui.lineEdit.text()
        QApplication.processEvents()
        if not path.exists(folder):
            if QMessageBox.critical(self, self.tr("Folder does not exists"), self.tr("Selected folder")+" "+folder+" "+self.tr("does not exists.\n\nDo you want to create it?"), QMessageBox.No, QMessageBox.Ok) == QMessageBox.Ok:
                system("mkdir -p "+str(folder))
                if not path.exists(str(folder)):
                    QMessageBox.critical(self, self.tr("Folder cannot be created"), self.tr("Selected folder")+" "+folder+" "*self.tr("cannot be created.\n\nCheck your permissions or use another folder"), QMessageBox.Ok)
                    process=False
            else:
                
                process=False
                self.boto_b_back_2()
        QApplication.processEvents()

        if process:
            global nomore
            QApplication.processEvents()
            self.actual=0
            self.total=self.ui.listWidget.count()
            nomore=False
            self.ui.b_sortir.setEnabled(0)
            self.ui.b_back_2.setVisible(0)
            self.ui.b_stop.setVisible(1)
            self.ui.b_sortir_2.setVisible(0)
         #fill process list with original listwidget
            self.ui.listWidget_2.clear()
            for i in range(self.total):
                item=self.ui.listWidget.item(i)
                a=QListWidgetItem(self.ui.listWidget_2)
                a.setText(item.text())
                a.setIcon(QIcon(self.soundIcon))
                self.ui.listWidget_2.addItem(a)
            QApplication.processEvents()
            mp3bitrate=str(self.ui.cb_bitrate.currentText())
            oggbitrate=int(self.ui.horizontalSlider.value())
            #process first
            self.processStepbyStep()


    def processStepbyStep(self):
        global item, file, format, mp3bitrate, oggbitrate, folder, nomore, formats, onlyfile, fileWOextension

        if not nomore:
            file=self.ui.listWidget_2.item(self.actual).text()
            item=self.ui.listWidget_2.item(self.actual)
            format=formats[self.ui.cb_format.currentIndex()]
            item.setIcon(QIcon(self.processIcon))
            #print self.ui.cb_bitrate.currentItem()

            #print file[-3:].lower()
            if file[-3:].toLower()==format:
            #if it's already on desired format, ignore it
                item.setIcon(QIcon(self.inoredIcon))
                item.setText(self.tr("Ignored: File already on format")+" - "+file)
                self.completed()

            else:
            #if it's on the path with desired format, ignore it
                #onlyfile=getoutput('basename "'+str(file)+'"')
                onlyfile=path.basename(str(file.toLocal8Bit()))
                fileWOextension=onlyfile[:-3]
                if path.exists(str(QString(folder+"/"+fileWOextension+format).toLocal8Bit())):
                    item.setIcon(QIcon(self.inoredIconTarget))
                    item.setText(self.tr("Ignored: File already converted")+" - "+file)
                    self.completed()
            #else process it
                else:
                    #print "processing"
                    self.process = ConvertFile()
                    self.connect(self.process,SIGNAL("FirstCompleted"),self.signalFirst)
                    #self.connect(self.process,SIGNAL("FinalCompleted"),self.completed)
                    self.connect(self.process,SIGNAL("finished()"),self.signalCompleted)
                    self.process.start()

    def signalCompleted(self):
        item.setIcon(QIcon(self.okIcon))
        item.setText(self.tr("Complete:")+" - "+file)
        self.completed()

    def signalFirst(self):
        #print "first step"
        item.setIcon(QIcon(self.process2Icon))

    def completed(self):
        global nomore
        #print "finished"
        if not nomore:
            #print "another file"
            self.actual=self.actual+1
            #print self.actual
            #print self.total
            if self.actual<self.total:
                #print "process another"
                self.processStepbyStep()
            else:
                print "it's the end of the list as we know it ^_^"
                self.ui.b_back_2.setVisible(1)
                self.ui.b_sortir_2.setVisible(1)
                self.ui.b_stop.setVisible(0)
                self.ui.b_sortir.setEnabled(1)
                QMessageBox.information(self, self.tr("¡¡¡Conversion Completed!!!"), self.tr("Finish. All files were converted!"), QMessageBox.Ok )
        #else:
            #print "nomore - process stoped"

    def stop(self):
        global nomore
        if QMessageBox.critical(self, self.tr("Stop process?"), self.tr("Are you sure to stop the conversion process?"), QMessageBox.No, QMessageBox.Ok) == QMessageBox.Ok:
            nomore=True
            self.process.stop()
            self.process.terminate()
            self.ui.b_back_2.setVisible(1)
            self.ui.b_sortir_2.setVisible(1)
            self.ui.b_stop.setVisible(0)
            self.ui.b_sortir.setEnabled(1)
            item.setIcon(QIcon(self.stopedIcon))

    def boto_b_back_2(self):
        self.ui.b_sortir.setEnabled(1)
        self.ui.pages.setCurrentIndex(1)

class ConvertFile(QThread):
    def __init__(self):
        QThread.__init__(self)
        #self.run()

    def run(self):

        global item, file, format, mp3bitrate, oggbitrate, tmpfile, nomore, onlyfile, fileWOextension, globalpath
        nomore=False

        #print file
        #if not self.linksupport:  #if 0 == yes linksupport - it's an echo && echo $? 0 -> OK
        system("rm -f /tmp/audioconversor-tmp-file /tmp/audiodump.wav")
        #system('ln -s "'+file+'" '+tmpfile)

        #midi support
        if file[-4:].toLower()=='.mid' or file[-4:].toLower()=='.kar' or file[-5:].toLower()=='.midi':
            system('timidity -Ow "'+str(file.toLocal8Bit())+'"')
            system('mv "'+str(file[:-3].toLocal8Bit())+'"wav /tmp/audiodump.wav')
        else:
            symlink(str(file.toLocal8Bit()), tmpfile)

            self.engega=QProcess()
            self.engega.start("sh "+globalpath+"/scripts/convert_to_standard")
        #self.engega.start('cd /tmp ; mplayer -ao pcm "/tmp/audioconversor-tmp-file" -vo null')

            if not self.engega.waitForFinished(2 * 60 * 1000): #wait for 2 hours
                print "DONE"
        self.emit(SIGNAL("FirstCompleted"))

        self.engega=QProcess()
        
        dest=str(QString(folder+'/'+fileWOextension+format).toLocal8Bit())
        #print dest

        if not nomore:
            if format=="wav":
                #system("mv /tmp/audiodump.wav '"+str(folder)+"/"+fileWOextension+str(format)+"'")
                #self.engega.start('mv, /tmp/audiodump.wav "'+str(folder)+'/'+fileWOextension+str(format)+'"')
                rename("/tmp/audiodump.wav", dest)
                if not self.engega.waitForFinished(2 * 60 * 1000): #wait for 2 hours
                    print "DoNe 2"

            elif format=="mp3":
                self.engega.start("lame -b "+str(mp3bitrate)+" /tmp/audiodump.wav")

                if not self.engega.waitForFinished(2 * 60 * 1000): #wait for 2 hours
                    print "DoNe 2"

                if not nomore:
                    #system('mv /tmp/audiodump.wav.mp3 "'+str(folder)+'/'+fileWOextension+str(format)+'"')
                    rename("/tmp/audiodump.wav.mp3", dest)

            elif format=="ogg":

                #system("scripts/convert_to_ogg "+str(oggbitrate))
                #self.engega.start("scripts/convert_to_ogg "+str(oggbitrate))
                self.engega.start("oggenc -q  "+str(oggbitrate)+" /tmp/audiodump.wav")
                if not self.engega.waitForFinished(2 * 60 * 1000): #wait for 2 hours
                    print "DoNe 2"

                if not nomore:
                    #system('mv /tmp/audiodump.ogg "'+str(folder)+'/'+fileWOextension+str(format)+'"')
                    rename("/tmp/audiodump.ogg", dest)


        if not nomore:
            self.emit(SIGNAL("FinalCompleted"))

        system("rm -f /tmp/audioconversor-tmp-file")

    def stop(self):
        global nomore
        nomore=True
        self.engega.kill()
        #print "terminated"
        self.terminate()



app = QApplication(sys.argv)

locale = QLocale.system().name()
qtTranslator = QTranslator()
if qtTranslator.load("/usr/share/kademar/utils/audioconversor/tr/"+locale.split("_")[0]+".qm"):
    app.installTranslator(qtTranslator)
    print "Loaded "+locale
elif qtTranslator.load("/usr/share/kademar/utils/audioconversor/tr/en.qm"):
    app.installTranslator(qtTranslator)
    print "Loaded "+locale

qtTranslatorQT = QTranslator()
qtTranslatorQT.load("qt_"+locale, "/usr/share/qt4/translations")
app.installTranslator(qtTranslatorQT)

AudioConversor = AudioConversor()
AudioConversor.show()
app.exec_()
