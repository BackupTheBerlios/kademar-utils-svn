#ifndef QRADIOBUTTONWITHEVENTS_H
#define QRADIOBUTTONWITHEVENTS_H

#include <QRadioButton>

class QRadioButtonWithEvents : public QRadioButton
{
    Q_OBJECT
public:
    explicit QRadioButtonWithEvents(QWidget *parent = 0);

public slots:
    void readCaption( QString * label );
    void buttonClickedFunction();

private:
    void enterEvent( QEvent * event );
    void focusInEvent( QFocusEvent * event );

};

#endif // QRADIOBUTTONWITHEVENTS_H
