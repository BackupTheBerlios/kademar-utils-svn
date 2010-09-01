#include "desktopselector.h"
#include "ui_desktopselector.h"
#include "qdesktopwidget.h"
#include "qpixmap.h"
#include "qfile.h"
#include "qmessagebox.h"
#include "qstring.h"
#include <qtextstream.h>
#include <qprocess.h>


DesktopSelector::DesktopSelector(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::DesktopSelector)
{
    ui->setupUi(this);
    this->setConnects();
    this->setMaxResolution();
    this->removeDesktops();
    //Use detect-monitor to configure it
    QProcess *dresol = new QProcess();
    dresol->start(QString("/usr/share/kademar/scripts/engegada/detect-monitor"));
    QString label = tr("Select the desktop you want to use");
    QProcess *readcommand = new QProcess();
    readcommand->start(QString("spd-say \"%1\"").arg(label));
}


DesktopSelector::~DesktopSelector()
{
    delete ui;
}

void DesktopSelector::changeEvent(QEvent *e)
{
    QMainWindow::changeEvent(e);
    switch (e->type()) {
    case QEvent::LanguageChange:
        ui->retranslateUi(this);
        break;
    default:
        break;
    }
}

void DesktopSelector::setConnects()
{
    //connect(ui->generalAction, SIGNAL(triggered()), this, SLOT(changeView()));
    connect(ui->b_kde3, SIGNAL(clicked()), this, SLOT(startDesktopKde3()));
    connect(ui->b_kde4, SIGNAL(clicked()), this, SLOT(startDesktopKde4()));
    connect(ui->b_lxde, SIGNAL(clicked()), this, SLOT(startDesktopLxde()));
    connect(ui->b_gnome, SIGNAL(clicked()), this, SLOT(startDesktopGnome()));
    connect(ui->b_icewm, SIGNAL(clicked()), this, SLOT(startDesktopIcewm()));
    connect(ui->b_shutdown, SIGNAL(clicked()), this, SLOT(askForShutdown()));
}


void DesktopSelector::askForShutdown()
{
    QString label = tr("Are you sure to shutdown the computer?");
    QProcess *readcommand = new QProcess();
    readcommand->start(QString("spd-say \"%1\"").arg(label));
    QMessageBox *dial = new QMessageBox();
    dial->setWindowTitle(tr("Shutdown Computer"));
    dial->setText(label);
    dial->setStandardButtons(QMessageBox::No | QMessageBox::Yes);
    dial->setDefaultButton(QMessageBox::No );
    if (dial->exec() == QMessageBox::Yes) {
        QFile *file = new QFile("/var/tmp/xsession-commands");
        //QTextStream *stream = new QTextStream();
        if ( file->open( QIODevice::WriteOnly ) )
        {
            QTextStream stream( file );
            stream << "shutdown halt force\n";
        }
        file->close();

        QFile *file2 = new QFile("/var/tmp/xserver");
        //QTextStream *stream2 = new QTextStream();
        if ( file2->open( QIODevice::Append ) )
        {
            QTextStream stream2( file2 );
            stream2 << "DESKTOP=none\n";
        }
        file2->close();

        this->close();
    }
}

void DesktopSelector::setMaxResolution()
{
    QDesktopWidget qDesktopWidget;
    QRect screenSize = qDesktopWidget.screenGeometry();
    //qDebug() << screenSize.width();
    DesktopSelector::setGeometry(0,0,screenSize.width(),screenSize.height());
    ui->background->setGeometry(0,0,screenSize.width(),screenSize.height());
    QFile *filebg = new QFile(QString("/usr/share/wallpapers/Ethais/contents/images/%1x%2.png").arg(screenSize.width()).arg(screenSize.height()) );
    if  (!(filebg->exists())) {

        filebg->setFileName(QString("/usr/share/wallpapers/Ethais/contents/images/1280x1024.png"));
    }

    if  (!(filebg->exists())) {

        filebg->setFileName(QString("/usr/share/wallpapers/kademar.png"));
    }

    ui->background->setPixmap(QPixmap(filebg->fileName()));

}

void DesktopSelector::removeDesktops()
{
    QFile *desktop = new QFile();
    //KDE3
    desktop->setFileName(QString("/opt/kde3/bin/startkde"));
    if  (!(desktop->exists())) {
            ui->b_kde3->setVisible(0);
            ui->l_kde3->setVisible(0);
    }
    //KDE4
    desktop->setFileName(QString("/usr/bin/startkde"));
    if  (!(desktop->exists())) {
            ui->b_kde4->setVisible(0);
            ui->l_kde4->setVisible(0);
    }
    //GNOME
    desktop->setFileName(QString("/usr/bin/startgnome"));
    if  (!(desktop->exists())) {
            ui->b_gnome->setVisible(0);
            ui->l_gnome->setVisible(0);
    }
    //LXDE
    desktop->setFileName(QString("/usr/bin/startlxde"));
    if  (!(desktop->exists())) {
            ui->b_lxde->setVisible(0);
            ui->l_lxde->setVisible(0);
    }
    //ICEWM
    desktop->setFileName(QString("/usr/bin/starticewm"));
    if  (!(desktop->exists())) {
            ui->b_icewm->setVisible(0);
            ui->l_icewm->setVisible(0);
    }
}



// Desktop Starter
void DesktopSelector::startDesktopKde3()
{
    QFile *file = new QFile("/var/tmp/xserver");
    //QTextStream *stream = new QTextStream();
    if ( file->open( QIODevice::Append ) )
    {
        QTextStream stream( file );
        stream << "DESKTOP=kde3\n";
    }
    file->close();
    this->close();
}

void DesktopSelector::startDesktopKde4()
{
    QFile *file = new QFile("/var/tmp/xserver");
    //QTextStream *stream = new QTextStream();
    if ( file->open( QIODevice::Append ) )
    {
        QTextStream stream( file );
        stream << "DESKTOP=kde4\n";
    }
    file->close();
    this->close();
}

void DesktopSelector::startDesktopGnome()
{
    QFile *file = new QFile("/var/tmp/xserver");
    //QTextStream *stream = new QTextStream();
    if ( file->open( QIODevice::Append ) )
    {
        QTextStream stream( file );
        stream << "DESKTOP=gnome\n";
    }
    file->close();
    this->close();
}

void DesktopSelector::startDesktopLxde()
{
    QFile *file = new QFile("/var/tmp/xserver");
    //QTextStream *stream = new QTextStream();
    if ( file->open( QIODevice::Append ) )
    {
        QTextStream stream( file );
        stream << "DESKTOP=lxde\n";
    }
    file->close();
    this->close();
}

void DesktopSelector::startDesktopIcewm()
{
    QFile *file = new QFile("/var/tmp/xserver");
    //QTextStream *stream = new QTextStream();
    if ( file->open( QIODevice::Append ) )
    {
        QTextStream stream( file );
        stream << "DESKTOP=icewm\n";
    }
    file->close();
    this->close();
}
