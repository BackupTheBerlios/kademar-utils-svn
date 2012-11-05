/********************************************************************************
** Form generated from reading UI file 'desktopselector.ui'
**
** Created: Mon Jul 30 23:01:01 2012
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
    QFrame *displayFrame;
    QGridLayout *gridLayout_7;
    QSpacerItem *horizontalSpacer_9;
    QLabel *displayDetectedLabel;
    QFrame *advancedConfigurationFrame;
    QGridLayout *gridLayout_5;
    QComboBoxWithEvents *cb_chipset;
    QLabel *label;
    QSpacerItem *horizontalSpacer_6;
    QLabel *l_resol;
    QSliderWithEvents *hslider_resolutions;
    QCheckBoxWithEvents *ch_forceResol;
    QCheckBoxWithEvents *ch_forceDriver;
    QPushButtonWithEvents *b_startDesktop;
    QLabel *displayChipetLabel;
    QFrame *driverFrame;
    QGridLayout *gridLayout_6;
    QRadioButtonWithEvents *rb_propietaryDriver;
    QRadioButtonWithEvents *rb_freeDriver;
    QPushButtonWithEvents *b_previous;
    QSpacerItem *verticalSpacer_5;
    QSpacerItem *horizontalSpacer_7;
    QSpacerItem *horizontalSpacer_8;
    QSpacerItem *verticalSpacer_6;
    QWidget *accessibilityPage;
    QGridLayout *gridLayout_15;
    QLabel *accessibilityLabel;
    QFrame *accessibilityFrame;
    QGridLayout *gridLayout_14;
    QGroupBox *advancedAccessibilityGroupBox;
    QGridLayout *gridLayout_11;
    QCheckBox *checkBox;
    QCheckBox *checkBox_2;
    QCheckBox *checkBox_4;
    QCheckBox *checkBox_5;
    QPushButton *pushButton;
    QCheckBox *checkBox_6;
    QCheckBox *checkBox_7;
    QCheckBox *checkBox_8;
    QCheckBox *checkBox_9;
    QCheckBox *checkBox_10;
    QCheckBox *checkBox_3;
    QSpacerItem *horizontalSpacer_15;
    QPushButton *pushButton_2;
    QGroupBox *groupBox;
    QGridLayout *gridLayout_13;
    QPushButton *pushButton_4;
    QPushButton *pushButton_9;
    QPushButton *pushButton_6;
    QPushButton *pushButton_7;
    QPushButton *pushButton_8;
    QSpacerItem *horizontalSpacer_16;
    QPushButton *pushButton_3;
    QPushButton *pushButton_5;
    QSpacerItem *verticalSpacer_11;
    QSpacerItem *verticalSpacer_12;
    QSpacerItem *horizontalSpacer_13;
    QSpacerItem *horizontalSpacer_14;
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
    QFrame *controlFrame;
    QGridLayout *gridLayout_2;
    QPushButtonWithEvents *b_accessibility;
    QPushButtonWithEvents *b_desktop;
    QPushButtonWithEvents *b_shutdown;
    QSpacerItem *horizontalSpacer_3;
    QPushButtonWithEvents *b_language;
    QPushButtonWithEvents *b_configuration;
    QMenuBar *menuBar;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *DesktopSelector)
    {
        if (DesktopSelector->objectName().isEmpty())
            DesktopSelector->setObjectName(QString::fromUtf8("DesktopSelector"));
        DesktopSelector->resize(884, 484);
        centralWidget = new QWidget(DesktopSelector);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        gridLayout = new QGridLayout(centralWidget);
        gridLayout->setSpacing(6);
        gridLayout->setContentsMargins(11, 11, 11, 11);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
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

        displayFrame = new QFrame(displayPage);
        displayFrame->setObjectName(QString::fromUtf8("displayFrame"));
        displayFrame->setMinimumSize(QSize(450, 250));
        displayFrame->setFrameShape(QFrame::StyledPanel);
        displayFrame->setFrameShadow(QFrame::Raised);
        gridLayout_7 = new QGridLayout(displayFrame);
        gridLayout_7->setSpacing(6);
        gridLayout_7->setContentsMargins(11, 11, 11, 11);
        gridLayout_7->setObjectName(QString::fromUtf8("gridLayout_7"));
        horizontalSpacer_9 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_7->addItem(horizontalSpacer_9, 6, 3, 1, 1);

        displayDetectedLabel = new QLabel(displayFrame);
        displayDetectedLabel->setObjectName(QString::fromUtf8("displayDetectedLabel"));
        displayDetectedLabel->setMaximumSize(QSize(16777215, 50));
        QFont font1;
        font1.setBold(true);
        font1.setWeight(75);
        displayDetectedLabel->setFont(font1);
        displayDetectedLabel->setAlignment(Qt::AlignLeading|Qt::AlignLeft|Qt::AlignVCenter);

        gridLayout_7->addWidget(displayDetectedLabel, 0, 0, 1, 5);

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

        horizontalSpacer_6 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_5->addItem(horizontalSpacer_6, 3, 2, 1, 1);

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


        gridLayout_7->addWidget(advancedConfigurationFrame, 4, 0, 1, 5);

        b_startDesktop = new QPushButtonWithEvents(displayFrame);
        b_startDesktop->setObjectName(QString::fromUtf8("b_startDesktop"));
        QIcon icon;
        icon.addFile(QString::fromUtf8(":/img/img/ok.png"), QSize(), QIcon::Normal, QIcon::Off);
        b_startDesktop->setIcon(icon);
        b_startDesktop->setIconSize(QSize(32, 32));

        gridLayout_7->addWidget(b_startDesktop, 6, 4, 1, 1);

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


        gridLayout_7->addWidget(driverFrame, 3, 1, 1, 4);

        b_previous = new QPushButtonWithEvents(displayFrame);
        b_previous->setObjectName(QString::fromUtf8("b_previous"));
        b_previous->setMinimumSize(QSize(0, 32));
        QIcon icon1;
        icon1.addFile(QString::fromUtf8(":/img/img/go-previous.png"), QSize(), QIcon::Normal, QIcon::Off);
        b_previous->setIcon(icon1);
        b_previous->setIconSize(QSize(32, 22));

        gridLayout_7->addWidget(b_previous, 6, 2, 1, 1);


        gridLayout_8->addWidget(displayFrame, 4, 1, 1, 1);

        verticalSpacer_5 = new QSpacerItem(447, 104, QSizePolicy::Minimum, QSizePolicy::Expanding);

        gridLayout_8->addItem(verticalSpacer_5, 5, 1, 1, 1);

        horizontalSpacer_7 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_8->addItem(horizontalSpacer_7, 4, 2, 1, 1);

        horizontalSpacer_8 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_8->addItem(horizontalSpacer_8, 4, 0, 1, 1);

        verticalSpacer_6 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        gridLayout_8->addItem(verticalSpacer_6, 0, 1, 1, 1);

        stackedWidget->addWidget(displayPage);
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

        pushButton = new QPushButton(advancedAccessibilityGroupBox);
        pushButton->setObjectName(QString::fromUtf8("pushButton"));
        pushButton->setIcon(icon1);

        gridLayout_11->addWidget(pushButton, 12, 0, 1, 1);

        checkBox_6 = new QCheckBox(advancedAccessibilityGroupBox);
        checkBox_6->setObjectName(QString::fromUtf8("checkBox_6"));

        gridLayout_11->addWidget(checkBox_6, 5, 0, 1, 4);

        checkBox_7 = new QCheckBox(advancedAccessibilityGroupBox);
        checkBox_7->setObjectName(QString::fromUtf8("checkBox_7"));

        gridLayout_11->addWidget(checkBox_7, 7, 0, 1, 4);

        checkBox_8 = new QCheckBox(advancedAccessibilityGroupBox);
        checkBox_8->setObjectName(QString::fromUtf8("checkBox_8"));

        gridLayout_11->addWidget(checkBox_8, 8, 0, 1, 4);

        checkBox_9 = new QCheckBox(advancedAccessibilityGroupBox);
        checkBox_9->setObjectName(QString::fromUtf8("checkBox_9"));

        gridLayout_11->addWidget(checkBox_9, 9, 0, 1, 4);

        checkBox_10 = new QCheckBox(advancedAccessibilityGroupBox);
        checkBox_10->setObjectName(QString::fromUtf8("checkBox_10"));

        gridLayout_11->addWidget(checkBox_10, 10, 0, 1, 4);

        checkBox_3 = new QCheckBox(advancedAccessibilityGroupBox);
        checkBox_3->setObjectName(QString::fromUtf8("checkBox_3"));

        gridLayout_11->addWidget(checkBox_3, 2, 0, 1, 4);

        horizontalSpacer_15 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_11->addItem(horizontalSpacer_15, 12, 1, 1, 2);

        pushButton_2 = new QPushButton(advancedAccessibilityGroupBox);
        pushButton_2->setObjectName(QString::fromUtf8("pushButton_2"));
        pushButton_2->setLayoutDirection(Qt::RightToLeft);
        QIcon icon2;
        icon2.addFile(QString::fromUtf8(":/img/img/go-next.png"), QSize(), QIcon::Normal, QIcon::Off);
        pushButton_2->setIcon(icon2);

        gridLayout_11->addWidget(pushButton_2, 12, 3, 1, 1);


        gridLayout_14->addWidget(advancedAccessibilityGroupBox, 1, 1, 1, 1);

        groupBox = new QGroupBox(accessibilityFrame);
        groupBox->setObjectName(QString::fromUtf8("groupBox"));
        gridLayout_13 = new QGridLayout(groupBox);
        gridLayout_13->setSpacing(6);
        gridLayout_13->setContentsMargins(11, 11, 11, 11);
        gridLayout_13->setObjectName(QString::fromUtf8("gridLayout_13"));
        pushButton_4 = new QPushButton(groupBox);
        pushButton_4->setObjectName(QString::fromUtf8("pushButton_4"));

        gridLayout_13->addWidget(pushButton_4, 0, 0, 1, 3);

        pushButton_9 = new QPushButton(groupBox);
        pushButton_9->setObjectName(QString::fromUtf8("pushButton_9"));

        gridLayout_13->addWidget(pushButton_9, 1, 0, 1, 3);

        pushButton_6 = new QPushButton(groupBox);
        pushButton_6->setObjectName(QString::fromUtf8("pushButton_6"));

        gridLayout_13->addWidget(pushButton_6, 3, 0, 1, 3);

        pushButton_7 = new QPushButton(groupBox);
        pushButton_7->setObjectName(QString::fromUtf8("pushButton_7"));

        gridLayout_13->addWidget(pushButton_7, 4, 0, 1, 3);

        pushButton_8 = new QPushButton(groupBox);
        pushButton_8->setObjectName(QString::fromUtf8("pushButton_8"));

        gridLayout_13->addWidget(pushButton_8, 5, 0, 1, 3);

        horizontalSpacer_16 = new QSpacerItem(128, 22, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_13->addItem(horizontalSpacer_16, 6, 0, 1, 2);

        pushButton_3 = new QPushButton(groupBox);
        pushButton_3->setObjectName(QString::fromUtf8("pushButton_3"));

        gridLayout_13->addWidget(pushButton_3, 6, 2, 1, 1);

        pushButton_5 = new QPushButton(groupBox);
        pushButton_5->setObjectName(QString::fromUtf8("pushButton_5"));

        gridLayout_13->addWidget(pushButton_5, 2, 0, 1, 3);


        gridLayout_14->addWidget(groupBox, 1, 0, 1, 1);


        gridLayout_15->addWidget(accessibilityFrame, 2, 1, 1, 1);

        verticalSpacer_11 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        gridLayout_15->addItem(verticalSpacer_11, 0, 1, 1, 1);

        verticalSpacer_12 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        gridLayout_15->addItem(verticalSpacer_12, 3, 1, 1, 1);

        horizontalSpacer_13 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_15->addItem(horizontalSpacer_13, 2, 2, 1, 1);

        horizontalSpacer_14 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_15->addItem(horizontalSpacer_14, 2, 0, 1, 1);

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
        QIcon icon3;
        icon3.addFile(QString::fromUtf8(":/img/img/system-reboot.png"), QSize(), QIcon::Normal, QIcon::Off);
        b_rebootComputer->setIcon(icon3);
        b_rebootComputer->setIconSize(QSize(40, 40));

        gridLayout_12->addWidget(b_rebootComputer, 1, 1, 1, 2);

        b_shutdownComputer = new QPushButtonWithEvents(shutdownFrame);
        b_shutdownComputer->setObjectName(QString::fromUtf8("b_shutdownComputer"));
        QIcon icon4;
        icon4.addFile(QString::fromUtf8(":/img/img/system-shutdown.png"), QSize(), QIcon::Normal, QIcon::Off);
        b_shutdownComputer->setIcon(icon4);
        b_shutdownComputer->setIconSize(QSize(40, 40));

        gridLayout_12->addWidget(b_shutdownComputer, 0, 1, 1, 2);

        b_cancel = new QPushButtonWithEvents(shutdownFrame);
        b_cancel->setObjectName(QString::fromUtf8("b_cancel"));
        QIcon icon5;
        icon5.addFile(QString::fromUtf8(":/img/img/dialog-cancel.png"), QSize(), QIcon::Normal, QIcon::Off);
        b_cancel->setIcon(icon5);
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
        QIcon icon6;
        icon6.addFile(QString::fromUtf8(":/img/img/accessibility.png"), QSize(), QIcon::Normal, QIcon::Off);
        b_accessibility->setIcon(icon6);
        b_accessibility->setIconSize(QSize(32, 32));

        gridLayout_2->addWidget(b_accessibility, 0, 3, 1, 1);

        b_desktop = new QPushButtonWithEvents(controlFrame);
        b_desktop->setObjectName(QString::fromUtf8("b_desktop"));
        b_desktop->setMinimumSize(QSize(0, 32));
        QIcon icon7;
        icon7.addFile(QString::fromUtf8(":/img/img/desktop.png"), QSize(), QIcon::Normal, QIcon::Off);
        b_desktop->setIcon(icon7);
        b_desktop->setIconSize(QSize(32, 32));

        gridLayout_2->addWidget(b_desktop, 0, 2, 1, 1);

        b_shutdown = new QPushButtonWithEvents(controlFrame);
        b_shutdown->setObjectName(QString::fromUtf8("b_shutdown"));
        b_shutdown->setMinimumSize(QSize(0, 32));
        b_shutdown->setMaximumSize(QSize(300, 16777215));
        b_shutdown->setIcon(icon4);
        b_shutdown->setIconSize(QSize(32, 22));

        gridLayout_2->addWidget(b_shutdown, 0, 6, 1, 1);

        horizontalSpacer_3 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_2->addItem(horizontalSpacer_3, 0, 5, 1, 1);

        b_language = new QPushButtonWithEvents(controlFrame);
        b_language->setObjectName(QString::fromUtf8("b_language"));
        b_language->setMinimumSize(QSize(0, 32));
        QIcon icon8;
        icon8.addFile(QString::fromUtf8(":/img/img/language.png"), QSize(), QIcon::Normal, QIcon::Off);
        b_language->setIcon(icon8);
        b_language->setIconSize(QSize(32, 32));

        gridLayout_2->addWidget(b_language, 0, 1, 1, 1);

        b_configuration = new QPushButtonWithEvents(controlFrame);
        b_configuration->setObjectName(QString::fromUtf8("b_configuration"));
        b_configuration->setMinimumSize(QSize(0, 32));
        QIcon icon9;
        icon9.addFile(QString::fromUtf8(":/img/img/advanced-configuration.png"), QSize(), QIcon::Normal, QIcon::Off);
        b_configuration->setIcon(icon9);
        b_configuration->setIconSize(QSize(32, 32));

        gridLayout_2->addWidget(b_configuration, 0, 4, 1, 1);


        gridLayout->addWidget(controlFrame, 3, 0, 1, 2);

        DesktopSelector->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(DesktopSelector);
        menuBar->setObjectName(QString::fromUtf8("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 884, 20));
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
        desktopLabel->setText(QApplication::translate("DesktopSelector", "Select the desktop you want to use", 0, QApplication::UnicodeUTF8));
        languageLabel->setText(QApplication::translate("DesktopSelector", "Select language you want to use", 0, QApplication::UnicodeUTF8));
        displayLabel->setText(QApplication::translate("DesktopSelector", "Select your display configuration", 0, QApplication::UnicodeUTF8));
        displayDetectedLabel->setText(QApplication::translate("DesktopSelector", "Detected", 0, QApplication::UnicodeUTF8));
        label->setText(QApplication::translate("DesktopSelector", "Advanced Configuration", 0, QApplication::UnicodeUTF8));
        l_resol->setText(QApplication::translate("DesktopSelector", "TextLabel", 0, QApplication::UnicodeUTF8));
        ch_forceResol->setText(QApplication::translate("DesktopSelector", "Force Display Resolution", 0, QApplication::UnicodeUTF8));
        ch_forceDriver->setText(QApplication::translate("DesktopSelector", "Force Display Driver", 0, QApplication::UnicodeUTF8));
        b_startDesktop->setText(QApplication::translate("DesktopSelector", "Start LiveCD Desktop", 0, QApplication::UnicodeUTF8));
        displayChipetLabel->setText(QString());
        rb_propietaryDriver->setText(QApplication::translate("DesktopSelector", "Use Propietary Graphic Driver (Recommended)", 0, QApplication::UnicodeUTF8));
        rb_freeDriver->setText(QApplication::translate("DesktopSelector", "Use Free Graphic Driver", 0, QApplication::UnicodeUTF8));
        b_previous->setText(QApplication::translate("DesktopSelector", "Previous", 0, QApplication::UnicodeUTF8));
        accessibilityLabel->setText(QApplication::translate("DesktopSelector", "Select Accessibility Options", 0, QApplication::UnicodeUTF8));
        advancedAccessibilityGroupBox->setTitle(QApplication::translate("DesktopSelector", "Advanced Selection", 0, QApplication::UnicodeUTF8));
        checkBox->setText(QApplication::translate("DesktopSelector", "Screenreader", 0, QApplication::UnicodeUTF8));
        checkBox_2->setText(QApplication::translate("DesktopSelector", "Screen Magnifier", 0, QApplication::UnicodeUTF8));
        checkBox_4->setText(QApplication::translate("DesktopSelector", "Mouse Assistant", 0, QApplication::UnicodeUTF8));
        checkBox_5->setText(QApplication::translate("DesktopSelector", "Mouse Gestures", 0, QApplication::UnicodeUTF8));
        pushButton->setText(QApplication::translate("DesktopSelector", "Simple Selection", 0, QApplication::UnicodeUTF8));
        checkBox_6->setText(QApplication::translate("DesktopSelector", "Handwritten Write", 0, QApplication::UnicodeUTF8));
        checkBox_7->setText(QApplication::translate("DesktopSelector", "Webcam Mouse Movement", 0, QApplication::UnicodeUTF8));
        checkBox_8->setText(QApplication::translate("DesktopSelector", "Window Assistant", 0, QApplication::UnicodeUTF8));
        checkBox_9->setText(QApplication::translate("DesktopSelector", "Predictive Text", 0, QApplication::UnicodeUTF8));
        checkBox_10->setText(QApplication::translate("DesktopSelector", "Multimedia Keyboard Assistant", 0, QApplication::UnicodeUTF8));
        checkBox_3->setText(QApplication::translate("DesktopSelector", "Virtual Keyboard", 0, QApplication::UnicodeUTF8));
        pushButton_2->setText(QApplication::translate("DesktopSelector", "Next", 0, QApplication::UnicodeUTF8));
        groupBox->setTitle(QApplication::translate("DesktopSelector", "Simple Selection", 0, QApplication::UnicodeUTF8));
        pushButton_4->setText(QApplication::translate("DesktopSelector", "Sight difficults without useful part", 0, QApplication::UnicodeUTF8));
        pushButton_9->setText(QApplication::translate("DesktopSelector", "Reduced mobility on arms and hands", 0, QApplication::UnicodeUTF8));
        pushButton_6->setText(QApplication::translate("DesktopSelector", "Old people", 0, QApplication::UnicodeUTF8));
        pushButton_7->setText(QApplication::translate("DesktopSelector", "Sight difficults with useful part", 0, QApplication::UnicodeUTF8));
        pushButton_8->setText(QApplication::translate("DesktopSelector", "Learning difficults", 0, QApplication::UnicodeUTF8));
        pushButton_3->setText(QApplication::translate("DesktopSelector", "Advanced Selection", 0, QApplication::UnicodeUTF8));
        pushButton_5->setText(QApplication::translate("DesktopSelector", "Without difficults", 0, QApplication::UnicodeUTF8));
        l_shutdown->setText(QApplication::translate("DesktopSelector", "Are you sure to shutdown the computer?", 0, QApplication::UnicodeUTF8));
        b_rebootComputer->setText(QApplication::translate("DesktopSelector", "Reboot Computer", 0, QApplication::UnicodeUTF8));
        b_shutdownComputer->setText(QApplication::translate("DesktopSelector", "Shutdown Computer", 0, QApplication::UnicodeUTF8));
        b_cancel->setText(QApplication::translate("DesktopSelector", "Cancel", 0, QApplication::UnicodeUTF8));
        label_2->setText(QString());
        b_accessibility->setText(QApplication::translate("DesktopSelector", "Accessibility", 0, QApplication::UnicodeUTF8));
        b_desktop->setText(QApplication::translate("DesktopSelector", "Desktop", 0, QApplication::UnicodeUTF8));
        b_shutdown->setText(QApplication::translate("DesktopSelector", "Shutdown Computer", 0, QApplication::UnicodeUTF8));
        b_language->setText(QApplication::translate("DesktopSelector", "Language", 0, QApplication::UnicodeUTF8));
        b_configuration->setText(QApplication::translate("DesktopSelector", "Configuration", 0, QApplication::UnicodeUTF8));
    } // retranslateUi

};

namespace Ui {
    class DesktopSelector: public Ui_DesktopSelector {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_DESKTOPSELECTOR_H
