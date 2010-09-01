#ifndef QPUSHBUTTONWITHEVENTS_H
#define QPUSHBUTTONWITHEVENTS_H

#include <QPushButton>

class QPushButtonWithEvents : public QPushButton
{
    Q_OBJECT
public:
    explicit QPushButtonWithEvents(QWidget *parent = 0);

signals:

public slots:
    void readCaption( QString * label );

private:
    void enterEvent( QEvent * event );

};

#endif // QPUSHBUTTONWITHEVENTS_H
