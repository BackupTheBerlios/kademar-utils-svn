/********************************************************************************
** Form generated from reading UI file 'helioxhelper.ui'
**
** Created: Mon Jul 30 21:25:42 2012
**      by: Qt User Interface Compiler version 4.8.2
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_HELIOXHELPER_H
#define UI_HELIOXHELPER_H

#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtGui/QApplication>
#include <QtGui/QButtonGroup>
#include <QtGui/QGridLayout>
#include <QtGui/QHeaderView>
#include <QtGui/QWidget>

QT_BEGIN_NAMESPACE

class Ui_HelioxHelper
{
public:
    QGridLayout *gridLayout;

    void setupUi(QWidget *HelioxHelper)
    {
        if (HelioxHelper->objectName().isEmpty())
            HelioxHelper->setObjectName(QString::fromUtf8("HelioxHelper"));
        HelioxHelper->resize(400, 300);
        gridLayout = new QGridLayout(HelioxHelper);
        gridLayout->setSpacing(6);
        gridLayout->setContentsMargins(0, 0, 0, 0);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));

        retranslateUi(HelioxHelper);

        QMetaObject::connectSlotsByName(HelioxHelper);
    } // setupUi

    void retranslateUi(QWidget *HelioxHelper)
    {
        HelioxHelper->setWindowTitle(QApplication::translate("HelioxHelper", "HelioxHelper", 0, QApplication::UnicodeUTF8));
    } // retranslateUi

};

namespace Ui {
    class HelioxHelper: public Ui_HelioxHelper {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_HELIOXHELPER_H
