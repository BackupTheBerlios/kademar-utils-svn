#-------------------------------------------------
#
# Project created by QtCreator 2012-06-07T18:02:28
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = HelioxHelper
TEMPLATE = app

#CONFIG += console

TRANSLATIONS = tr/es_ES.ts tr/es_MX.ts tr/ca_ES.ts tr/gl_ES.ts tr/eu_ES.ts

SOURCES += main.cpp\
        helioxhelper.cpp \
    writeConfig.cpp \
    qtoolbuttonwithevents.cpp \
    SingleApplication.cpp \
    qactionwithevents.cpp \
    wideiconsmenu.cpp

HEADERS  += helioxhelper.h \
    writeConfig.h \
    qtoolbuttonwithevents.h \
    SingleApplication.h \
    qactionwithevents.h \
    wideiconsmenu.h

FORMS    += helioxhelper.ui \
    about.ui

RESOURCES += \
    Resource.qrc

OTHER_FILES += \
    ToDo.txt \
    tr/gl_ES.ts \
    tr/eu_ES.ts \
    tr/es_ES.ts \
    tr/ca_ES.ts \
    tr/es_MX.ts
