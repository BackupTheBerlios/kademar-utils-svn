/********************************************************************************
** Form generated from reading UI file 'desktopselector.ui'
**
** Created: Wed Aug 1 22:12:22 2012
**      by: Qt User Interface Compiler version 4.8.2
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_DESKTOPSELECTOR_H
#define UI_DESKTOPSELECTOR_H

#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtGui/QApplication>
#include <QtGui/QButtonGroup>
#include <QtGui/QCheckBox>
#include <QtGui/QFrame>
#include <QtGui/QGridLayout>
#include <QtGui/QGroupBox>
#include <QtGui/QHeaderView>
#include <QtGui/QLabel>
#include <QtGui/QMainWindow>
#include <QtGui/QMenuBar>
#include <QtGui/QPushButton>
#include <QtGui/QSpacerItem>
#include <QtGui/QStackedWidget>
#include <QtGui/QStatusBar>
#include <QtGui/QWidget>
#include <qcheckboxwithevents.h>
#include <qcomboboxwithevents.h>
#include <qpushbuttonwithevents.h>
#include <qradiobuttonwithevents.h>
#include <qsliderwithevents.h>

QT_BEGIN_NAMESPACE

class Ui_DesktopSelector
{
public:
    QWidget *centralWidget;
    QGridLayout *gridLayout;
    QFrame *controlFrame;
    QGridLayout *gridLayout_2;
    QPushButtonWithEvents *b_accessibility;
    QSpacerItem *horizontalSpacer_3;
    QPushButtonWithEvents *b_desktop;
    QPushButtonWithEvents *b_shutdown;
    QPushButtonWithEvents *b_language;
    QPushButtonWithEvents *b_previous;
    QPushButtonWithEvents *b_displayConfiguration;
    QStackedWidget *stackedWidget;
    QWidget *desktopPage;
    QGridLayout *gridLayout_4;
    QSpacerItem *verticalSpacer_2;
    QLabel *desktopLabel;
    QSpacerItem *horizontalSpacer;
    QSpacerItem *horizontalSpacer_2;
    QSpacerItem *verticalSpacer;
    QFrame *desktopFrame;
    QWidget *languagePage;
    QGridLayout *gridLayout_3;
    QLabel *languageLabel;
    QSpacerItem *horizontalSpacer_5;
    QFrame *languageFrame;
    QSpacerItem *horizontalSpacer_4;
    QSpacerItem *verticalSpacer_4;
    QSpacerItem *verticalSpacer_3;
    QWidget *displayPage;
    QGridLayout *gridLayout_8;
    QLabel *displayLabel;
    QSpacerItem *verticalSpacer_5;
    QSpacerItem *horizontalSpacer_8;
    QSpacerItem *horizontalSpacer_7;
    QSpacerItem *verticalSpacer_6;
    QFrame *displayFrame;
    QGridLayout *gridLayout_7;
    QLabel *displayDetectedLabel;
    QLabel *displayChipetLabel;
    QFrame *driverFrame;
    QGridLayout *gridLayout_6;
    QRadioButtonWithEvents *rb_propietaryDriver;
    QRadioButtonWithEvents *rb_freeDriver;
    QPushButtonWithEvents *b_startDesktop;
    QPushButtonWithEvents *b_displayAccept;
    QFrame *advancedConfigurationFrame;
    QGridLayout *gridLayout_5;
    QComboBoxWithEvents *cb_chipset;
    QLabel *label;
    QLabel *l_resol;
    QSliderWithEvents *hslider_resolutions;
    QCheckBoxWithEvents *ch_forceResol;
    QCheckBoxWithEvents *ch_forceDriver;
    QSpacerItem *horizontalSpacer_6;
    QSpacerItem *horizontalSpacer_9;
    QPushButtonWithEvents *b_displayPrevious;
    QWidget *selectUserPage;
    QGridLayout *gridLayout_19;
    QSpacerItem *verticalSpacer_13;
    QLabel *userLabel;
    QSpacerItem *horizontalSpacer_19;
    QFrame *userFrame;
    QGridLayout *gridLayout_16;
    QSpacerItem *horizontalSpacer_20;
    QSpacerItem *verticalSpacer_14;
    QWidget *accessibilityPage;
    QGridLayout *gridLayout_15;
    QLabel *accessibilityLabel;
    QSpacerItem *horizontalSpacer_14;
    QSpacerItem *verticalSpacer_11;
    QSpacerItem *verticalSpacer_12;
    QSpacerItem *horizontalSpacer_13;
    QFrame *accessibilityFrame;
    QGridLayout *gridLayout_14;
    QGroupBox *advancedAccessibilityGroupBox;
    QGridLayout *gridLayout_11;
    QCheckBox *checkBox_9;
    QCheckBox *checkBox;
    QCheckBox *checkBox_2;
    QCheckBox *checkBox_4;
    QCheckBox *checkBox_5;
    QCheckBox *checkBox_6;
    QCheckBox *checkBox_7;
    QCheckBox *checkBox_8;
    QCheckBox *checkBox_10;
    QCheckBox *checkBox_3;
    QPushButton *b_accessibilitySimpleSelection;
    QSpacerItem *horizontalSpacer_18;
    QFrame *frame_2;
    QGridLayout *gridLayout_20;
    QSpacerItem *horizontalSpacer_21;
    QPushButtonWithEvents *b_accessibilityPrevious2;
    QPushButtonWithEvents *b_accessibilityAccept2;
    QGroupBox *simpleAccessibilityGroupBox;
    QGridLayout *gridLayout_13;
    QPushButton *pushButton_4;
    QPushButton *pushButton_9;
    QPushButton *pushButton_6;
    QPushButton *pushButton_7;
    QPushButton *pushButton_8;
    QSpacerItem *horizontalSpacer_16;
    QPushButton *pushButton_5;
    QPushButton *b_advancedAccessibility;
    QFrame *frame;
    QGridLayout *gridLayout_18;
    QSpacerItem *horizontalSpacer_15;
    QPushButtonWithEvents *b_accessibilityPrevious1;
    QPushButtonWithEvents *b_accessibilityAccept1;
    QWidget *shutdownPage;
    QGridLayout *gridLayout_10;
    QSpacerItem *verticalSpacer_7;
    QLabel *l_shutdown;
    QSpacerItem *horizontalSpacer_11;
    QSpacerItem *horizontalSpacer_10;
    QSpacerItem *verticalSpacer_8;
    QFrame *shutdownFrame;
    QGridLayout *gridLayout_9;
    QGridLayout *gridLayout_12;
    QPushButtonWithEvents *b_rebootComputer;
    QPushButtonWithEvents *b_shutdownComputer;
    QPushButtonWithEvents *b_cancel;
    QSpacerItem *horizontalSpacer_12;
    QLabel *label_2;
    QSpacerItem *verticalSpacer_9;
    QSpacerItem *verticalSpacer_10;
    QMenuBar *menuBar;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *DesktopSelector)
    {
        if (DesktopSelector->objectName().isEmpty())
            DesktopSelector->setObjectName(QString::fromUtf8("DesktopSelector"));
        DesktopSelector->resize(1135, 570);
        centralWidget = new QWidget(DesktopSelector);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        gridLayout = new QGridLayout(centralWidget);
        gridLayout->setSpacing(6);
        gridLayout->setContentsMargins(11, 11, 11, 11);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        controlFrame = new QFrame(centralWidget);
        controlFrame->setObjectName(QString::fromUtf8("controlFrame"));
        controlFrame->setMinimumSize(QSize(0, 70));
        controlFrame->setMaximumSize(QSize(16777215, 70));
        controlFrame->setFrameShape(QFrame::StyledPanel);
        controlFrame->setFrameShadow(QFrame::Raised);
        gridLayout_2 = new QGridLayout(controlFrame);
        gridLayout_2->setSpacing(6);
        gridLayout_2->setContentsMargins(11, 11, 11, 11);
        gridLayout_2->setObjectName(QString::fromUtf8("gridLayout_2"));
        b_accessibility = new QPushButtonWithEvents(controlFrame);
        b_accessibility->setObjectName(QString::fromUtf8("b_accessibility"));
        b_accessibility->setMinimumSize(QSize(0, 32));
        QIcon icon;
        icon.addFile(QString::fromUtf8(":/img/img/accessibility.png"), QSize(), QIcon::Normal, QIcon::Off);
        b_accessibility->setIcon(icon);
        b_accessibility->setIconSize(QSize(32, 32));

        gridLayout_2->addWidget(b_accessibility, 0, 3, 1, 1);

        horizontalSpacer_3 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_2->addItem(horizontalSpacer_3, 0, 5, 1, 1);

        b_desktop = new QPushButtonWithEvents(controlFrame);
        b_desktop->setObjectName(QString::fromUtf8("b_desktop"));
        b_desktop->setMinimumSize(QSize(0, 32));
        QIcon icon1;
        icon1.addFile(QString::fromUtf8(":/img/img/desktop.png"), QSize(), QIcon::Normal, QIcon::Off);
        b_desktop->setIcon(icon1);
        b_desktop->setIconSize(QSize(32, 32));

        gridLayout_2->addWidget(b_desktop, 0, 2, 1, 1);

        b_shutdown = new QPushButtonWithEvents(controlFrame);
        b_shutdown->setObjectName(QString::fromUtf8("b_shutdown"));
        b_shutdown->setMinimumSize(QSize(0, 32));
        b_shutdown->setMaximumSize(QSize(300, 16777215));
        QIcon icon2;
        icon2.addFile(QString::fromUtf8(":/img/img/system-shutdown.png"), QSize(), QIcon::Normal, QIcon::Off);
        b_shutdown->setIcon(icon2);
        b_shutdown->setIconSize(QSize(32, 22));

        gridLayout_2->addWidget(b_shutdown, 0, 6, 1, 1);

        b_language = new QPushButtonWithEvents(controlFrame);
        b_language->setObjectName(QString::fromUtf8("b_language"));
        b_language->setMinimumSize(QSize(0, 32));
        QIcon icon3;
        icon3.addFile(QString::fromUtf8(":/img/img/language.png"), QSize(), QIcon::Normal, QIcon::Off);
        b_language->setIcon(icon3);
        b_language->setIconSize(QSize(32, 32));

        gridLayout_2->addWidget(b_language, 0, 1, 1, 1);

        b_previous = new QPushButtonWithEvents(controlFrame);
        b_previous->setObjectName(QString::fromUtf8("b_previous"));
        b_previous->setMinimumSize(QSize(0, 32));
        QIcon icon4;
        icon4.addFile(QString::fromUtf8(":/img/img/go-previous.png"), QSize(), QIcon::Normal, QIcon::Off);
        b_previous->setIcon(icon4);
        b_previous->setIconSize(QSize(32, 32));

        gridLayout_2->addWidget(b_previous, 0, 0, 1, 1);

        b_displayConfiguration = new QPushButtonWithEvents(controlFrame);
        b_displayConfiguration->setObjectName(QString::fromUtf8("b_displayConfiguration"));
        b_displayConfiguration->setMinimumSize(QSize(0, 32));
        QIcon icon5;
        icon5.addFile(QString::fromUtf8(":/img/img/advanced-configuration.png"), QSize(), QIcon::Normal, QIcon::Off);
        b_displayConfiguration->setIcon(icon5);
        b_displayConfiguration->setIconSize(QSize(32, 32));

        gridLayout_2->addWidget(b_displayConfiguration, 0, 4, 1, 1);


        gridLayout->addWidget(controlFrame, 3, 0, 1, 2);

        stackedWidget = new QStackedWidget(centralWidget);
        stackedWidget->setObjectName(QString::fromUtf8("stackedWidget"));
        desktopPage = new QWidget();
        desktopPage->setObjectName(QString::fromUtf8("desktopPage"));
        gridLayout_4 = new QGridLayout(desktopPage);
        gridLayout_4->setSpacing(6);
        gridLayout_4->setContentsMargins(11, 11, 11, 11);
        gridLayout_4->setObjectName(QString::fromUtf8("gridLayout_4"));
        verticalSpacer_2 = new QSpacerItem(20, 67, QSizePolicy::Minimum, QSizePolicy::Expanding);

        gridLayout_4->addItem(verticalSpacer_2, 0, 1, 1, 1);

        desktopLabel = new QLabel(desktopPage);
        desktopLabel->setObjectName(QString::fromUtf8("desktopLabel"));
        QFont font;
        font.setPointSize(11);
        font.setBold(true);
        font.setItalic(true);
        font.setWeight(75);
        desktopLabel->setFont(font);
        desktopLabel->setAlignment(Qt::AlignCenter);

        gridLayout_4->addWidget(desktopLabel, 1, 1, 1, 1);

        horizontalSpacer = new QSpacerItem(259, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_4->addItem(horizontalSpacer, 2, 0, 1, 1);

        horizontalSpacer_2 = new QSpacerItem(258, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_4->addItem(horizontalSpacer_2, 2, 2, 1, 1);

        verticalSpacer = new QSpacerItem(20, 66, QSizePolicy::Minimum, QSizePolicy::Expanding);

        gridLayout_4->addItem(verticalSpacer, 3, 1, 1, 1);

        desktopFrame = new QFrame(desktopPage);
        desktopFrame->setObjectName(QString::fromUtf8("desktopFrame"));
        desktopFrame->setFrameShape(QFrame::StyledPanel);
        desktopFrame->setFrameShadow(QFrame::Raised);

        gridLayout_4->addWidget(desktopFrame, 2, 1, 1, 1);

        stackedWidget->addWidget(desktopPage);
        languagePage = new QWidget();
        languagePage->setObjectName(QString::fromUtf8("languagePage"));
        gridLayout_3 = new QGridLayout(languagePage);
        gridLayout_3->setSpacing(6);
        gridLayout_3->setContentsMargins(11, 11, 11, 11);
        gridLayout_3->setObjectName(QString::fromUtf8("gridLayout_3"));
        languageLabel = new QLabel(languagePage);
        languageLabel->setObjectName(QString::fromUtf8("languageLabel"));
        languageLabel->setFont(font);
        languageLabel->setAlignment(Qt::AlignCenter);

        gridLayout_3->addWidget(languageLabel, 1, 1, 1, 1);

        horizontalSpacer_5 = new QSpacerItem(241, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_3->addItem(horizontalSpacer_5, 2, 0, 1, 1);

        languageFrame = new QFrame(languagePage);
        languageFrame->setObjectName(QString::fromUtf8("languageFrame"));
        languageFrame->setFrameShape(QFrame::StyledPanel);
        languageFrame->setFrameShadow(QFrame::Raised);

        gridLayout_3->addWidget(languageFrame, 2, 1, 1, 1);

        horizontalSpacer_4 = new QSpacerItem(240, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_3->addItem(horizontalSpacer_4, 2, 2, 1, 1);

        verticalSpacer_4 = new QSpacerItem(20, 194, QSizePolicy::Minimum, QSizePolicy::Expanding);

        gridLayout_3->addItem(verticalSpacer_4, 3, 1, 1, 1);

        verticalSpacer_3 = new QSpacerItem(20, 194, QSizePolicy::Minimum, QSizePolicy::Expanding);

        gridLayout_3->addItem(verticalSpacer_3, 0, 1, 1, 1);

        stackedWidget->addWidget(languagePage);
        displayPage = new QWidget();
        displayPage->setObjectName(QString::fromUtf8("displayPage"));
        gridLayout_8 = new QGridLayout(displayPage);
        gridLayout_8->setSpacing(6);
        gridLayout_8->setContentsMargins(11, 11, 11, 11);
        gridLayout_8->setObjectName(QString::fromUtf8("gridLayout_8"));
        displayLabel = new QLabel(displayPage);
        displayLabel->setObjectName(QString::fromUtf8("displayLabel"));
        displayLabel->setFont(font);
        displayLabel->setAlignment(Qt::AlignCenter);

        gridLayout_8->addWidget(displayLabel, 1, 1, 1, 1);

        verticalSpacer_5 = new QSpacerItem(447, 104, QSizePolicy::Minimum, QSizePolicy::Expanding);

        gridLayout_8->addItem(verticalSpacer_5, 5, 1, 1, 1);

        horizontalSpacer_8 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_8->addItem(horizontalSpacer_8, 4, 0, 1, 1);

        horizontalSpacer_7 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_8->addItem(horizontalSpacer_7, 4, 2, 1, 1);

        verticalSpacer_6 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        gridLayout_8->addItem(verticalSpacer_6, 0, 1, 1, 1);

        displayFrame = new QFrame(displayPage);
        displayFrame->setObjectName(QString::fromUtf8("displayFrame"));
        displayFrame->setMinimumSize(QSize(450, 250));
        displayFrame->setFrameShape(QFrame::StyledPanel);
        displayFrame->setFrameShadow(QFrame::Raised);
        gridLayout_7 = new QGridLayout(displayFrame);
        gridLayout_7->setSpacing(6);
        gridLayout_7->setContentsMargins(11, 11, 11, 11);
        gridLayout_7->setObjectName(QString::fromUtf8("gridLayout_7"));
        displayDetectedLabel = new QLabel(displayFrame);
        displayDetectedLabel->setObjectName(QString::fromUtf8("displayDetectedLabel"));
        displayDetectedLabel->setMaximumSize(QSize(16777215, 50));
        QFont font1;
        font1.setBold(true);
        font1.setWeight(75);
        displayDetectedLabel->setFont(font1);
        displayDetectedLabel->setAlignment(Qt::AlignLeading|Qt::AlignLeft|Qt::AlignVCenter);

        gridLayout_7->addWidget(displayDetectedLabel, 0, 0, 1, 6);

        displayChipetLabel = new QLabel(displayFrame);
        displayChipetLabel->setObjectName(QString::fromUtf8("displayChipetLabel"));
        displayChipetLabel->setMinimumSize(QSize(64, 64));
        displayChipetLabel->setMaximumSize(QSize(68, 68));
        displayChipetLabel->setPixmap(QPixmap(QString::fromUtf8(":/img/img/display.png")));
        displayChipetLabel->setScaledContents(true);

        gridLayout_7->addWidget(displayChipetLabel, 3, 0, 1, 1);

        driverFrame = new QFrame(displayFrame);
        driverFrame->setObjectName(QString::fromUtf8("driverFrame"));
        driverFrame->setFrameShape(QFrame::StyledPanel);
        driverFrame->setFrameShadow(QFrame::Raised);
        gridLayout_6 = new QGridLayout(driverFrame);
        gridLayout_6->setSpacing(6);
        gridLayout_6->setContentsMargins(11, 11, 11, 11);
        gridLayout_6->setObjectName(QString::fromUtf8("gridLayout_6"));
        rb_propietaryDriver = new QRadioButtonWithEvents(driverFrame);
        rb_propietaryDriver->setObjectName(QString::fromUtf8("rb_propietaryDriver"));
        rb_propietaryDriver->setChecked(true);

        gridLayout_6->addWidget(rb_propietaryDriver, 0, 0, 1, 1);

        rb_freeDriver = new QRadioButtonWithEvents(driverFrame);
        rb_freeDriver->setObjectName(QString::fromUtf8("rb_freeDriver"));

        gridLayout_6->addWidget(rb_freeDriver, 1, 0, 1, 1);


        gridLayout_7->addWidget(driverFrame, 3, 1, 1, 5);

        b_startDesktop = new QPushButtonWithEvents(displayFrame);
        b_startDesktop->setObjectName(QString::fromUtf8("b_startDesktop"));
        QIcon icon6;
        icon6.addFile(QString::fromUtf8(":/img/img/ok.png"), QSize(), QIcon::Normal, QIcon::Off);
        b_startDesktop->setIcon(icon6);
        b_startDesktop->setIconSize(QSize(32, 32));

        gridLayout_7->addWidget(b_startDesktop, 6, 5, 1, 1);

        b_displayAccept = new QPushButtonWithEvents(displayFrame);
        b_displayAccept->setObjectName(QString::fromUtf8("b_displayAccept"));
        b_displayAccept->setMinimumSize(QSize(0, 32));
        b_displayAccept->setIcon(icon6);
        b_displayAccept->setIconSize(QSize(32, 32));

        gridLayout_7->addWidget(b_displayAccept, 6, 4, 1, 1);

        advancedConfigurationFrame = new QFrame(displayFrame);
        advancedConfigurationFrame->setObjectName(QString::fromUtf8("advancedConfigurationFrame"));
        advancedConfigurationFrame->setFrameShape(QFrame::StyledPanel);
        advancedConfigurationFrame->setFrameShadow(QFrame::Raised);
        gridLayout_5 = new QGridLayout(advancedConfigurationFrame);
        gridLayout_5->setSpacing(6);
        gridLayout_5->setContentsMargins(11, 11, 11, 11);
        gridLayout_5->setObjectName(QString::fromUtf8("gridLayout_5"));
        cb_chipset = new QComboBoxWithEvents(advancedConfigurationFrame);
        cb_chipset->setObjectName(QString::fromUtf8("cb_chipset"));
        cb_chipset->setEnabled(false);
        QSizePolicy sizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
        sizePolicy.setHorizontalStretch(2);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(cb_chipset->sizePolicy().hasHeightForWidth());
        cb_chipset->setSizePolicy(sizePolicy);
        cb_chipset->setMaximumSize(QSize(150, 16777215));

        gridLayout_5->addWidget(cb_chipset, 3, 1, 1, 1);

        label = new QLabel(advancedConfigurationFrame);
        label->setObjectName(QString::fromUtf8("label"));
        label->setMaximumSize(QSize(16777215, 70));
        QFont font2;
        font2.setPointSize(11);
        font2.setBold(true);
        font2.setWeight(75);
        label->setFont(font2);
        label->setAlignment(Qt::AlignCenter);

        gridLayout_5->addWidget(label, 0, 1, 1, 5);

        l_resol = new QLabel(advancedConfigurationFrame);
        l_resol->setObjectName(QString::fromUtf8("l_resol"));
        l_resol->setEnabled(false);
        l_resol->setMinimumSize(QSize(80, 0));
#ifndef QT_NO_ACCESSIBILITY
        l_resol->setAccessibleName(QString::fromUtf8(""));
#endif // QT_NO_ACCESSIBILITY
        l_resol->setAlignment(Qt::AlignCenter);

        gridLayout_5->addWidget(l_resol, 3, 5, 1, 1);

        hslider_resolutions = new QSliderWithEvents(advancedConfigurationFrame);
        hslider_resolutions->setObjectName(QString::fromUtf8("hslider_resolutions"));
        hslider_resolutions->setEnabled(false);
        hslider_resolutions->setOrientation(Qt::Horizontal);

        gridLayout_5->addWidget(hslider_resolutions, 3, 4, 1, 1);

        ch_forceResol = new QCheckBoxWithEvents(advancedConfigurationFrame);
        ch_forceResol->setObjectName(QString::fromUtf8("ch_forceResol"));
        ch_forceResol->setFont(font1);

        gridLayout_5->addWidget(ch_forceResol, 1, 4, 1, 3);

        ch_forceDriver = new QCheckBoxWithEvents(advancedConfigurationFrame);
        ch_forceDriver->setObjectName(QString::fromUtf8("ch_forceDriver"));
        ch_forceDriver->setFont(font1);

        gridLayout_5->addWidget(ch_forceDriver, 1, 0, 1, 3);

        horizontalSpacer_6 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_5->addItem(horizontalSpacer_6, 3, 2, 1, 1);


        gridLayout_7->addWidget(advancedConfigurationFrame, 4, 0, 1, 6);

        horizontalSpacer_9 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_7->addItem(horizontalSpacer_9, 6, 3, 1, 1);

        b_displayPrevious = new QPushButtonWithEvents(displayFrame);
        b_displayPrevious->setObjectName(QString::fromUtf8("b_displayPrevious"));
        b_displayPrevious->setMinimumSize(QSize(0, 32));
        b_displayPrevious->setIcon(icon4);
        b_displayPrevious->setIconSize(QSize(32, 32));

        gridLayout_7->addWidget(b_displayPrevious, 6, 0, 1, 3);


        gridLayout_8->addWidget(displayFrame, 4, 1, 1, 1);

        stackedWidget->addWidget(displayPage);
        selectUserPage = new QWidget();
        selectUserPage->setObjectName(QString::fromUtf8("selectUserPage"));
        gridLayout_19 = new QGridLayout(selectUserPage);
        gridLayout_19->setSpacing(6);
        gridLayout_19->setContentsMargins(11, 11, 11, 11);
        gridLayout_19->setObjectName(QString::fromUtf8("gridLayout_19"));
        verticalSpacer_13 = new QSpacerItem(20, 34, QSizePolicy::Minimum, QSizePolicy::Expanding);

        gridLayout_19->addItem(verticalSpacer_13, 0, 1, 1, 1);

        userLabel = new QLabel(selectUserPage);
        userLabel->setObjectName(QString::fromUtf8("userLabel"));
        userLabel->setFont(font);
        userLabel->setAlignment(Qt::AlignCenter);

        gridLayout_19->addWidget(userLabel, 1, 1, 1, 1);

        horizontalSpacer_19 = new QSpacerItem(200, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_19->addItem(horizontalSpacer_19, 2, 0, 1, 1);

        userFrame = new QFrame(selectUserPage);
        userFrame->setObjectName(QString::fromUtf8("userFrame"));
        userFrame->setMinimumSize(QSize(450, 250));
        userFrame->setFrameShape(QFrame::StyledPanel);
        userFrame->setFrameShadow(QFrame::Raised);
        gridLayout_16 = new QGridLayout(userFrame);
        gridLayout_16->setSpacing(6);
        gridLayout_16->setContentsMargins(11, 11, 11, 11);
        gridLayout_16->setObjectName(QString::fromUtf8("gridLayout_16"));

        gridLayout_19->addWidget(userFrame, 2, 1, 1, 1);

        horizontalSpacer_20 = new QSpacerItem(200, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_19->addItem(horizontalSpacer_20, 2, 2, 1, 1);

        verticalSpacer_14 = new QSpacerItem(20, 35, QSizePolicy::Minimum, QSizePolicy::Expanding);

        gridLayout_19->addItem(verticalSpacer_14, 3, 1, 1, 1);

        stackedWidget->addWidget(selectUserPage);
        accessibilityPage = new QWidget();
        accessibilityPage->setObjectName(QString::fromUtf8("accessibilityPage"));
        gridLayout_15 = new QGridLayout(accessibilityPage);
        gridLayout_15->setSpacing(6);
        gridLayout_15->setContentsMargins(11, 11, 11, 11);
        gridLayout_15->setObjectName(QString::fromUtf8("gridLayout_15"));
        accessibilityLabel = new QLabel(accessibilityPage);
        accessibilityLabel->setObjectName(QString::fromUtf8("accessibilityLabel"));
        accessibilityLabel->setFont(font);
        accessibilityLabel->setAlignment(Qt::AlignCenter);

        gridLayout_15->addWidget(accessibilityLabel, 1, 1, 1, 1);

        horizontalSpacer_14 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_15->addItem(horizontalSpacer_14, 2, 0, 1, 1);

        verticalSpacer_11 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        gridLayout_15->addItem(verticalSpacer_11, 0, 1, 1, 1);

        verticalSpacer_12 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        gridLayout_15->addItem(verticalSpacer_12, 3, 1, 1, 1);

        horizontalSpacer_13 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_15->addItem(horizontalSpacer_13, 2, 2, 1, 1);

        accessibilityFrame = new QFrame(accessibilityPage);
        accessibilityFrame->setObjectName(QString::fromUtf8("accessibilityFrame"));
        accessibilityFrame->setFrameShape(QFrame::StyledPanel);
        accessibilityFrame->setFrameShadow(QFrame::Raised);
        gridLayout_14 = new QGridLayout(accessibilityFrame);
        gridLayout_14->setSpacing(6);
        gridLayout_14->setContentsMargins(11, 11, 11, 11);
        gridLayout_14->setObjectName(QString::fromUtf8("gridLayout_14"));
        advancedAccessibilityGroupBox = new QGroupBox(accessibilityFrame);
        advancedAccessibilityGroupBox->setObjectName(QString::fromUtf8("advancedAccessibilityGroupBox"));
        advancedAccessibilityGroupBox->setStyleSheet(QString::fromUtf8(""));
        gridLayout_11 = new QGridLayout(advancedAccessibilityGroupBox);
        gridLayout_11->setSpacing(6);
        gridLayout_11->setContentsMargins(11, 11, 11, 11);
        gridLayout_11->setObjectName(QString::fromUtf8("gridLayout_11"));
        checkBox_9 = new QCheckBox(advancedAccessibilityGroupBox);
        checkBox_9->setObjectName(QString::fromUtf8("checkBox_9"));

        gridLayout_11->addWidget(checkBox_9, 9, 0, 1, 4);

        checkBox = new QCheckBox(advancedAccessibilityGroupBox);
        checkBox->setObjectName(QString::fromUtf8("checkBox"));

        gridLayout_11->addWidget(checkBox, 0, 0, 1, 4);

        checkBox_2 = new QCheckBox(advancedAccessibilityGroupBox);
        checkBox_2->setObjectName(QString::fromUtf8("checkBox_2"));

        gridLayout_11->addWidget(checkBox_2, 1, 0, 1, 4);

        checkBox_4 = new QCheckBox(advancedAccessibilityGroupBox);
        checkBox_4->setObjectName(QString::fromUtf8("checkBox_4"));

        gridLayout_11->addWidget(checkBox_4, 4, 0, 1, 4);

        checkBox_5 = new QCheckBox(advancedAccessibilityGroupBox);
        checkBox_5->setObjectName(QString::fromUtf8("checkBox_5"));

        gridLayout_11->addWidget(checkBox_5, 6, 0, 1, 4);

        checkBox_6 = new QCheckBox(advancedAccessibilityGroupBox);
        checkBox_6->setObjectName(QString::fromUtf8("checkBox_6"));

        gridLayout_11->addWidget(checkBox_6, 5, 0, 1, 4);

        checkBox_7 = new QCheckBox(advancedAccessibilityGroupBox);
        checkBox_7->setObjectName(QString::fromUtf8("checkBox_7"));

        gridLayout_11->addWidget(checkBox_7, 7, 0, 1, 4);

        checkBox_8 = new QCheckBox(advancedAccessibilityGroupBox);
        checkBox_8->setObjectName(QString::fromUtf8("checkBox_8"));

        gridLayout_11->addWidget(checkBox_8, 8, 0, 1, 4);

        checkBox_10 = new QCheckBox(advancedAccessibilityGroupBox);
        checkBox_10->setObjectName(QString::fromUtf8("checkBox_10"));

        gridLayout_11->addWidget(checkBox_10, 10, 0, 1, 4);

        checkBox_3 = new QCheckBox(advancedAccessibilityGroupBox);
        checkBox_3->setObjectName(QString::fromUtf8("checkBox_3"));

        gridLayout_11->addWidget(checkBox_3, 2, 0, 1, 4);

        b_accessibilitySimpleSelection = new QPushButton(advancedAccessibilityGroupBox);
        b_accessibilitySimpleSelection->setObjectName(QString::fromUtf8("b_accessibilitySimpleSelection"));
        b_accessibilitySimpleSelection->setIcon(icon);

        gridLayout_11->addWidget(b_accessibilitySimpleSelection, 11, 0, 1, 1);

        horizontalSpacer_18 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_11->addItem(horizontalSpacer_18, 11, 3, 1, 1);

        frame_2 = new QFrame(advancedAccessibilityGroupBox);
        frame_2->setObjectName(QString::fromUtf8("frame_2"));
        frame_2->setFrameShape(QFrame::StyledPanel);
        frame_2->setFrameShadow(QFrame::Raised);
        gridLayout_20 = new QGridLayout(frame_2);
        gridLayout_20->setSpacing(6);
        gridLayout_20->setContentsMargins(11, 11, 11, 11);
        gridLayout_20->setObjectName(QString::fromUtf8("gridLayout_20"));
        horizontalSpacer_21 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_20->addItem(horizontalSpacer_21, 0, 1, 1, 1);

        b_accessibilityPrevious2 = new QPushButtonWithEvents(frame_2);
        b_accessibilityPrevious2->setObjectName(QString::fromUtf8("b_accessibilityPrevious2"));
        b_accessibilityPrevious2->setMinimumSize(QSize(150, 32));
        b_accessibilityPrevious2->setIcon(icon4);
        b_accessibilityPrevious2->setIconSize(QSize(32, 32));

        gridLayout_20->addWidget(b_accessibilityPrevious2, 0, 0, 1, 1);

        b_accessibilityAccept2 = new QPushButtonWithEvents(frame_2);
        b_accessibilityAccept2->setObjectName(QString::fromUtf8("b_accessibilityAccept2"));
        b_accessibilityAccept2->setMinimumSize(QSize(150, 32));
        b_accessibilityAccept2->setIcon(icon6);
        b_accessibilityAccept2->setIconSize(QSize(32, 32));

        gridLayout_20->addWidget(b_accessibilityAccept2, 0, 2, 1, 1);


        gridLayout_11->addWidget(frame_2, 12, 0, 1, 4);


        gridLayout_14->addWidget(advancedAccessibilityGroupBox, 1, 3, 1, 1);

        simpleAccessibilityGroupBox = new QGroupBox(accessibilityFrame);
        simpleAccessibilityGroupBox->setObjectName(QString::fromUtf8("simpleAccessibilityGroupBox"));
        gridLayout_13 = new QGridLayout(simpleAccessibilityGroupBox);
        gridLayout_13->setSpacing(6);
        gridLayout_13->setContentsMargins(11, 11, 11, 11);
        gridLayout_13->setObjectName(QString::fromUtf8("gridLayout_13"));
        pushButton_4 = new QPushButton(simpleAccessibilityGroupBox);
        pushButton_4->setObjectName(QString::fromUtf8("pushButton_4"));

        gridLayout_13->addWidget(pushButton_4, 0, 0, 1, 4);

        pushButton_9 = new QPushButton(simpleAccessibilityGroupBox);
        pushButton_9->setObjectName(QString::fromUtf8("pushButton_9"));

        gridLayout_13->addWidget(pushButton_9, 1, 0, 1, 4);

        pushButton_6 = new QPushButton(simpleAccessibilityGroupBox);
        pushButton_6->setObjectName(QString::fromUtf8("pushButton_6"));

        gridLayout_13->addWidget(pushButton_6, 3, 0, 1, 4);

        pushButton_7 = new QPushButton(simpleAccessibilityGroupBox);
        pushButton_7->setObjectName(QString::fromUtf8("pushButton_7"));

        gridLayout_13->addWidget(pushButton_7, 4, 0, 1, 4);

        pushButton_8 = new QPushButton(simpleAccessibilityGroupBox);
        pushButton_8->setObjectName(QString::fromUtf8("pushButton_8"));

        gridLayout_13->addWidget(pushButton_8, 5, 0, 1, 4);

        horizontalSpacer_16 = new QSpacerItem(128, 22, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_13->addItem(horizontalSpacer_16, 6, 0, 1, 2);

        pushButton_5 = new QPushButton(simpleAccessibilityGroupBox);
        pushButton_5->setObjectName(QString::fromUtf8("pushButton_5"));

        gridLayout_13->addWidget(pushButton_5, 2, 0, 1, 4);

        b_advancedAccessibility = new QPushButton(simpleAccessibilityGroupBox);
        b_advancedAccessibility->setObjectName(QString::fromUtf8("b_advancedAccessibility"));
        b_advancedAccessibility->setIcon(icon5);

        gridLayout_13->addWidget(b_advancedAccessibility, 6, 3, 1, 1);

        frame = new QFrame(simpleAccessibilityGroupBox);
        frame->setObjectName(QString::fromUtf8("frame"));
        frame->setFrameShape(QFrame::StyledPanel);
        frame->setFrameShadow(QFrame::Raised);
        gridLayout_18 = new QGridLayout(frame);
        gridLayout_18->setSpacing(6);
        gridLayout_18->setContentsMargins(11, 11, 11, 11);
        gridLayout_18->setObjectName(QString::fromUtf8("gridLayout_18"));
        horizontalSpacer_15 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_18->addItem(horizontalSpacer_15, 0, 1, 1, 1);

        b_accessibilityPrevious1 = new QPushButtonWithEvents(frame);
        b_accessibilityPrevious1->setObjectName(QString::fromUtf8("b_accessibilityPrevious1"));
        b_accessibilityPrevious1->setMinimumSize(QSize(150, 32));
        b_accessibilityPrevious1->setIcon(icon4);
        b_accessibilityPrevious1->setIconSize(QSize(32, 32));

        gridLayout_18->addWidget(b_accessibilityPrevious1, 0, 0, 1, 1);

        b_accessibilityAccept1 = new QPushButtonWithEvents(frame);
        b_accessibilityAccept1->setObjectName(QString::fromUtf8("b_accessibilityAccept1"));
        b_accessibilityAccept1->setMinimumSize(QSize(150, 32));
        b_accessibilityAccept1->setIcon(icon6);
        b_accessibilityAccept1->setIconSize(QSize(32, 32));

        gridLayout_18->addWidget(b_accessibilityAccept1, 0, 2, 1, 1);


        gridLayout_13->addWidget(frame, 7, 0, 1, 4);


        gridLayout_14->addWidget(simpleAccessibilityGroupBox, 1, 0, 1, 3);


        gridLayout_15->addWidget(accessibilityFrame, 2, 1, 1, 1);

        stackedWidget->addWidget(accessibilityPage);
        shutdownPage = new QWidget();
        shutdownPage->setObjectName(QString::fromUtf8("shutdownPage"));
        gridLayout_10 = new QGridLayout(shutdownPage);
        gridLayout_10->setSpacing(6);
        gridLayout_10->setContentsMargins(11, 11, 11, 11);
        gridLayout_10->setObjectName(QString::fromUtf8("gridLayout_10"));
        verticalSpacer_7 = new QSpacerItem(20, 149, QSizePolicy::Minimum, QSizePolicy::Expanding);

        gridLayout_10->addItem(verticalSpacer_7, 0, 1, 1, 1);

        l_shutdown = new QLabel(shutdownPage);
        l_shutdown->setObjectName(QString::fromUtf8("l_shutdown"));
        l_shutdown->setAlignment(Qt::AlignCenter);

        gridLayout_10->addWidget(l_shutdown, 1, 1, 1, 1);

        horizontalSpacer_11 = new QSpacerItem(230, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_10->addItem(horizontalSpacer_11, 2, 0, 1, 1);

        horizontalSpacer_10 = new QSpacerItem(229, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_10->addItem(horizontalSpacer_10, 2, 2, 1, 1);

        verticalSpacer_8 = new QSpacerItem(20, 149, QSizePolicy::Minimum, QSizePolicy::Expanding);

        gridLayout_10->addItem(verticalSpacer_8, 3, 1, 1, 1);

        shutdownFrame = new QFrame(shutdownPage);
        shutdownFrame->setObjectName(QString::fromUtf8("shutdownFrame"));
        shutdownFrame->setMinimumSize(QSize(350, 0));
        shutdownFrame->setFrameShape(QFrame::StyledPanel);
        shutdownFrame->setFrameShadow(QFrame::Raised);
        gridLayout_9 = new QGridLayout(shutdownFrame);
        gridLayout_9->setSpacing(6);
        gridLayout_9->setContentsMargins(11, 11, 11, 11);
        gridLayout_9->setObjectName(QString::fromUtf8("gridLayout_9"));
        gridLayout_12 = new QGridLayout();
        gridLayout_12->setSpacing(6);
        gridLayout_12->setObjectName(QString::fromUtf8("gridLayout_12"));
        b_rebootComputer = new QPushButtonWithEvents(shutdownFrame);
        b_rebootComputer->setObjectName(QString::fromUtf8("b_rebootComputer"));
        QIcon icon7;
        icon7.addFile(QString::fromUtf8(":/img/img/system-reboot.png"), QSize(), QIcon::Normal, QIcon::Off);
        b_rebootComputer->setIcon(icon7);
        b_rebootComputer->setIconSize(QSize(40, 40));

        gridLayout_12->addWidget(b_rebootComputer, 1, 1, 1, 2);

        b_shutdownComputer = new QPushButtonWithEvents(shutdownFrame);
        b_shutdownComputer->setObjectName(QString::fromUtf8("b_shutdownComputer"));
        b_shutdownComputer->setIcon(icon2);
        b_shutdownComputer->setIconSize(QSize(40, 40));

        gridLayout_12->addWidget(b_shutdownComputer, 0, 1, 1, 2);

        b_cancel = new QPushButtonWithEvents(shutdownFrame);
        b_cancel->setObjectName(QString::fromUtf8("b_cancel"));
        QIcon icon8;
        icon8.addFile(QString::fromUtf8(":/img/img/dialog-cancel.png"), QSize(), QIcon::Normal, QIcon::Off);
        b_cancel->setIcon(icon8);
        b_cancel->setIconSize(QSize(20, 20));

        gridLayout_12->addWidget(b_cancel, 2, 2, 1, 1);

        horizontalSpacer_12 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_12->addItem(horizontalSpacer_12, 2, 1, 1, 1);


        gridLayout_9->addLayout(gridLayout_12, 4, 2, 3, 1);

        label_2 = new QLabel(shutdownFrame);
        label_2->setObjectName(QString::fromUtf8("label_2"));
        label_2->setMaximumSize(QSize(64, 64));
        label_2->setPixmap(QPixmap(QString::fromUtf8(":/img/img/display.png")));
        label_2->setScaledContents(true);

        gridLayout_9->addWidget(label_2, 5, 0, 1, 1);

        verticalSpacer_9 = new QSpacerItem(20, 5, QSizePolicy::Minimum, QSizePolicy::Expanding);

        gridLayout_9->addItem(verticalSpacer_9, 4, 0, 1, 1);

        verticalSpacer_10 = new QSpacerItem(20, 51, QSizePolicy::Minimum, QSizePolicy::Expanding);

        gridLayout_9->addItem(verticalSpacer_10, 6, 0, 1, 1);


        gridLayout_10->addWidget(shutdownFrame, 2, 1, 1, 1);

        stackedWidget->addWidget(shutdownPage);

        gridLayout->addWidget(stackedWidget, 2, 0, 1, 1);

        DesktopSelector->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(DesktopSelector);
        menuBar->setObjectName(QString::fromUtf8("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 1135, 20));
        DesktopSelector->setMenuBar(menuBar);
        statusBar = new QStatusBar(DesktopSelector);
        statusBar->setObjectName(QString::fromUtf8("statusBar"));
        DesktopSelector->setStatusBar(statusBar);

        retranslateUi(DesktopSelector);

        stackedWidget->setCurrentIndex(2);


        QMetaObject::connectSlotsByName(DesktopSelector);
    } // setupUi

    void retranslateUi(QMainWindow *DesktopSelector)
    {
        DesktopSelector->setWindowTitle(QApplication::translate("DesktopSelector", "DesktopSelector", 0, QApplication::UnicodeUTF8));
        b_accessibility->setText(QApplication::translate("DesktopSelector", "Accessibility", 0, QApplication::UnicodeUTF8));
        b_desktop->setText(QApplication::translate("DesktopSelector", "Desktop", 0, QApplication::UnicodeUTF8));
        b_shutdown->setText(QApplication::translate("DesktopSelector", "Shutdown Computer", 0, QApplication::UnicodeUTF8));
        b_language->setText(QApplication::translate("DesktopSelector", "Language", 0, QApplication::UnicodeUTF8));
        b_previous->setText(QApplication::translate("DesktopSelector", "Previous", 0, QApplication::UnicodeUTF8));
        b_displayConfiguration->setText(QApplication::translate("DesktopSelector", "Configuration", 0, QApplication::UnicodeUTF8));
        desktopLabel->setText(QApplication::translate("DesktopSelector", "Select the desktop you want to use", 0, QApplication::UnicodeUTF8));
        languageLabel->setText(QApplication::translate("DesktopSelector", "Select language you want to use", 0, QApplication::UnicodeUTF8));
        displayLabel->setText(QApplication::translate("DesktopSelector", "Select your display configuration", 0, QApplication::UnicodeUTF8));
        displayDetectedLabel->setText(QApplication::translate("DesktopSelector", "Detected", 0, QApplication::UnicodeUTF8));
        displayChipetLabel->setText(QString());
        rb_propietaryDriver->setText(QApplication::translate("DesktopSelector", "Use Propietary Graphic Driver (Recommended)", 0, QApplication::UnicodeUTF8));
        rb_freeDriver->setText(QApplication::translate("DesktopSelector", "Use Free Graphic Driver", 0, QApplication::UnicodeUTF8));
        b_startDesktop->setText(QApplication::translate("DesktopSelector", "Start LiveCD Desktop", 0, QApplication::UnicodeUTF8));
        b_displayAccept->setText(QApplication::translate("DesktopSelector", "Accept", 0, QApplication::UnicodeUTF8));
        label->setText(QApplication::translate("DesktopSelector", "Advanced Configuration", 0, QApplication::UnicodeUTF8));
        l_resol->setText(QApplication::translate("DesktopSelector", "TextLabel", 0, QApplication::UnicodeUTF8));
        ch_forceResol->setText(QApplication::translate("DesktopSelector", "Force Display Resolution", 0, QApplication::UnicodeUTF8));
        ch_forceDriver->setText(QApplication::translate("DesktopSelector", "Force Display Driver", 0, QApplication::UnicodeUTF8));
        b_displayPrevious->setText(QApplication::translate("DesktopSelector", "Previous", 0, QApplication::UnicodeUTF8));
        userLabel->setText(QApplication::translate("DesktopSelector", "Select your user", 0, QApplication::UnicodeUTF8));
        accessibilityLabel->setText(QApplication::translate("DesktopSelector", "Select Accessibility Options", 0, QApplication::UnicodeUTF8));
        advancedAccessibilityGroupBox->setTitle(QApplication::translate("DesktopSelector", "Advanced Selection", 0, QApplication::UnicodeUTF8));
        checkBox_9->setText(QApplication::translate("DesktopSelector", "Predictive Text", 0, QApplication::UnicodeUTF8));
        checkBox->setText(QApplication::translate("DesktopSelector", "Screenreader", 0, QApplication::UnicodeUTF8));
        checkBox_2->setText(QApplication::translate("DesktopSelector", "Screen Magnifier", 0, QApplication::UnicodeUTF8));
        checkBox_4->setText(QApplication::translate("DesktopSelector", "Mouse Assistant", 0, QApplication::UnicodeUTF8));
        checkBox_5->setText(QApplication::translate("DesktopSelector", "Mouse Gestures", 0, QApplication::UnicodeUTF8));
        checkBox_6->setText(QApplication::translate("DesktopSelector", "Handwritten Write", 0, QApplication::UnicodeUTF8));
        checkBox_7->setText(QApplication::translate("DesktopSelector", "Webcam Mouse Movement", 0, QApplication::UnicodeUTF8));
        checkBox_8->setText(QApplication::translate("DesktopSelector", "Window Assistant", 0, QApplication::UnicodeUTF8));
        checkBox_10->setText(QApplication::translate("DesktopSelector", "Multimedia Keyboard Assistant", 0, QApplication::UnicodeUTF8));
        checkBox_3->setText(QApplication::translate("DesktopSelector", "Virtual Keyboard", 0, QApplication::UnicodeUTF8));
        b_accessibilitySimpleSelection->setText(QApplication::translate("DesktopSelector", "Simple Selection", 0, QApplication::UnicodeUTF8));
        b_accessibilityPrevious2->setText(QApplication::translate("DesktopSelector", "Previous", 0, QApplication::UnicodeUTF8));
        b_accessibilityAccept2->setText(QApplication::translate("DesktopSelector", "Accept", 0, QApplication::UnicodeUTF8));
        simpleAccessibilityGroupBox->setTitle(QApplication::translate("DesktopSelector", "Simple Selection", 0, QApplication::UnicodeUTF8));
        pushButton_4->setText(QApplication::translate("DesktopSelector", "Sight difficults without useful part", 0, QApplication::UnicodeUTF8));
        pushButton_9->setText(QApplication::translate("DesktopSelector", "Reduced mobility on arms and hands", 0, QApplication::UnicodeUTF8));
        pushButton_6->setText(QApplication::translate("DesktopSelector", "Old people", 0, QApplication::UnicodeUTF8));
        pushButton_7->setText(QApplication::translate("DesktopSelector", "Sight difficults with useful part", 0, QApplication::UnicodeUTF8));
        pushButton_8->setText(QApplication::translate("DesktopSelector", "Learning difficults", 0, QApplication::UnicodeUTF8));
        pushButton_5->setText(QApplication::translate("DesktopSelector", "Without difficults", 0, QApplication::UnicodeUTF8));
        b_advancedAccessibility->setText(QApplication::translate("DesktopSelector", "Advanced Selection", 0, QApplication::UnicodeUTF8));
        b_accessibilityPrevious1->setText(QApplication::translate("DesktopSelector", "Previous", 0, QApplication::UnicodeUTF8));
        b_accessibilityAccept1->setText(QApplication::translate("DesktopSelector", "Accept", 0, QApplication::UnicodeUTF8));
        l_shutdown->setText(QApplication::translate("DesktopSelector", "Are you sure to shutdown the computer?", 0, QApplication::UnicodeUTF8));
        b_rebootComputer->setText(QApplication::translate("DesktopSelector", "Reboot Computer", 0, QApplication::UnicodeUTF8));
        b_shutdownComputer->setText(QApplication::translate("DesktopSelector", "Shutdown Computer", 0, QApplication::UnicodeUTF8));
        b_cancel->setText(QApplication::translate("DesktopSelector", "Cancel", 0, QApplication::UnicodeUTF8));
        label_2->setText(QString());
    } // retranslateUi

};

namespace Ui {
    class DesktopSelector: public Ui_DesktopSelector {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_DESKTOPSELECTOR_H
