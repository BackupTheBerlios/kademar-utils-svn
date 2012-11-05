#ifndef QCHECKBOXWITHEVENTS_H
#define QCHECKBOXWITHEVENTS_H

#include <QCheckBox>

class QCheckBoxWithEvents : public QCheckBox
{
    Q_OBJECT
public:
    explicit QCheckBoxWithEvents(QWidget *parent = 0);

public slots:
    void readCaption( QString * label );
    void readClicked();

private:
    void enterEvent( QEvent * event );
    void focusInEvent( QFocusEvent * event );


};

#endif // QCHECKBOXWITHEVENTS_H
