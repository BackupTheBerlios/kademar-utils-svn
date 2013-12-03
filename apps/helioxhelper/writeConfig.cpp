#include <writeConfig.h>
#include <QSettings>
#include <QDebug>

/*

  Write initial settings if aren't

 */


void writeConfig()
{
    //extern QSettings settings;
    //QSettings settings("/home/clawlinux/desktop-selector.ini", QSettings::IniFormat);
    /*QDir *dir = new QDir;
    QFile *filebg = new QFile(QString("%1/config.ini").arg(QString(dir->currentPath())));
    if  (filebg->exists()) {
         QSettings settings(QString("%1/config.ini").arg(QString(dir->currentPath())));
         qDebug() << "Loading application settings";
    }*/
    /*filebg->setFileName(QString("%1/.config/HelioxHelper/config.ini").arg(QString(dir->homePath())));
    if  (filebg->exists()) {
         //QSettings settings(QString("%1/.config/HelioxHelper/config.ini").arg(QString(dir->homePath())));
         settings.setPath(QSettings::IniFormat, QSettings::UserScope, "HelioxHelper");
         //settings.setPath();
         qDebug() << "Loading home settings";
    }*/


    QSettings settings("ProyectoHeliox", "HelioxHelper");

    if (settings.value("General/autostart").toString() == ""){

        settings.beginGroup("General");
        settings.setValue("autostart", "1");
        settings.setValue("fullscreen", "0");
        settings.setValue("completeFullscreen", "0");
        settings.setValue("size", "350");
        settings.setValue("alwaysOnTop", "0");
        settings.setValue("alwaysOnBottom", "0");
        settings.setValue("whereIsPlacedWindow", "2");
        settings.setValue("closeConfirm", "1");
        settings.setValue("speechText", "1");
        settings.setValue("speechPath", "/usr/share/helioxhelper/speech");
        settings.setValue("fileLanguage", "en_US");
        settings.setValue("languageButtonDescription", "Choose your language");
        settings.endGroup();

        settings.beginGroup("Panel");
        settings.setValue("size", "350");
        settings.setValue("percentage", "90%");
        settings.setValue("align", "center");
        settings.endGroup();

        settings.beginGroup("Tray Icon");
        settings.setValue("showTrayIcon", "1");
        settings.setValue("leftClickContextualMenu", "0");
        //settings.setValue("rightClickContextualMenu", "1");
        settings.endGroup();


        settings.beginGroup("Contextual Menu");
        settings.setValue("showMinimize", "1");
        settings.setValue("showRestore", "0");
        settings.setValue("showSettings", "1");
        settings.setValue("showExit", "1");
        settings.endGroup();

        settings.beginGroup("Background");
        settings.setValue("wallpaperBackground", "0");
        settings.setValue("backgroundPath", "");
        settings.setValue("gradientBackground", "1");
        settings.setValue("gradientOrientation", "0");
        settings.setValue("gradientBeginColor", "#8bc9de");
        settings.setValue("gradientEndColor", "#ffffff");
        settings.endGroup();

        settings.beginGroup("Round Corners");
        settings.setValue("autoBorders", "1");
        settings.setValue("roundedMargin", "25");
        settings.setValue("top-left", "1");
        settings.setValue("top-right", "0");
        settings.setValue("bottom-left", "1");
        settings.setValue("bottom-right", "0");
        settings.endGroup();

        settings.beginGroup("App Buttons");
        settings.setValue("imageSize", "32");
        settings.setValue("iconAbove", "1");
        settings.setValue("showLabels", "true");
        settings.setValue("minimumHeight", "40");
        settings.setValue("maximumHeight", "0");
        settings.setValue("minimumWidth", "100");
        settings.setValue("maximumWidth", "0");
        settings.setValue("pixelsBorderNormal", "1");
        settings.setValue("pixelsBorderFocused", "2");
        settings.setValue("pixelsRoundedBorder", "10");
        settings.setValue("borderColorNormal", "#7d7d7d");
        settings.setValue("borderColorFocused", "#679cd0");
        settings.setValue("borderColorHovered", "#679cd0");
        settings.setValue("gradientBeginColor", "#e3e2e1");
        settings.setValue("gradientEndColor", "#cac9c8");
        settings.setValue("fontSize", "13");
        settings.endGroup();

        settings.beginGroup("Applications");
        settings.sync();

        qDebug() << "Writting default Settings";

        settings.beginWriteArray("app");
        settings.setArrayIndex(0);
        settings.setValue("name", "LibreOffice");
        settings.setValue("icon", "/usr/share/icons/hicolor/48x48/apps/libreoffice-startcenter.png");
        settings.setValue("desc", "Write your documents");
        settings.setValue("exec", "libreoffice");
        settings.setArrayIndex(1);
        settings.setValue("name", "FireFox");
        settings.setValue("icon", "/usr/share/icons/hicolor/48x48/apps/firefox.png");
        settings.setValue("desc", "Browse the web");
        settings.setValue("exec", "firefox");
        settings.setArrayIndex(2);
        settings.setValue("name", "newRow");
        settings.setValue("icon", "");
        settings.setValue("desc", "");
        settings.setValue("exec", "");
        settings.setArrayIndex(3);
        settings.setValue("name", "VLC");
        settings.setValue("icon", "/usr/share/icons/hicolor/48x48/apps/vlc.png");
        settings.setValue("desc", "Video and Music Mediaplayer");
        settings.setValue("exec", "vlc");
        settings.setArrayIndex(4);
        settings.setValue("name", "Pidgin");
        settings.setValue("icon", "/usr/share/icons/hicolor/48x48/apps/pidgin.png");
        settings.setValue("desc", "Multi Instant Messenger");
        settings.setValue("exec", "pidgin");
        settings.endArray();
        settings.endGroup();


    }
}
