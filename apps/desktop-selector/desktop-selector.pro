# -------------------------------------------------
# Project created by QtCreator 2010-06-08T13:33:48
# -------------------------------------------------
QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = desktop-selector
TEMPLATE = app
SOURCES += main.cpp \
    desktopselector.cpp \
    qpushbuttonwithevents.cpp \
    qradiobuttonwithevents.cpp \
    qcomboboxwithevents.cpp \
    qcheckboxwithevents.cpp \
    qsliderwithevents.cpp \
    wideiconsmenu.cpp \
    qactionwithevents.cpp \
    qtoolbuttonwithevents.cpp
HEADERS += desktopselector.h \
    qpushbuttonwithevents.h \
    qradiobuttonwithevents.h \
    qcomboboxwithevents.h \
    qcheckboxwithevents.h \
    qsliderwithevents.h \
    wideiconsmenu.h \
    qactionwithevents.h \
    qtoolbuttonwithevents.h
FORMS += desktopselector.ui
RESOURCES += resource.qrc
TRANSLATIONS = tr/es_ES.ts tr/es_MX.ts tr/myn_MX.ts tr/nah_MX.ts tr/ca_ES.ts tr/en.ts tr/gl_ES.ts tr/eu_ES.ts

OTHER_FILES += \
    TODO \
    scripts/nvidia-installer-offline.sh \
    scripts/ati-installer-offline.sh \
    scripts/locale_configurator \
    rc.d/desktop-selector \
    systemd/desktop-selector.service \
    xinit/lxde \
    xinit/kde4 \
    xinit/desktop-selector \
    xorg.conf.d/10-monitor.conf \
    xinit/enlightenment17 \
    tr/ca_ES.ts \
    tr/es_ES.ts \
    tr/gl_ES.ts \
    tr/eu_ES.ts \
    tr/es_MX.ts \
    tr/myn_MX.ts \
    tr/nah_MX.ts
