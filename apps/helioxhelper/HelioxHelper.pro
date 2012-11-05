#-------------------------------------------------
#
# Project created by QtCreator 2012-06-07T18:02:28
#
#-------------------------------------------------

QT       += gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = HelioxHelper
TEMPLATE = app

CONFIG += console


SOURCES += main.cpp\
        helioxhelper.cpp \
    writeConfig.cpp \
    qtoolbuttonwithevents.cpp \
    SingleApplication.cpp \

HEADERS  += helioxhelper.h \
    writeConfig.h \
    qtoolbuttonwithevents.h \
    SingleApplication.h

FORMS    += helioxhelper.ui

RESOURCES += \
    Resource.qrc

OTHER_FILES += \
    ToDo.txt \
    speech/vlc.ogg \
    speech/pidgin.ogg \
    speech/firefox.ogg
