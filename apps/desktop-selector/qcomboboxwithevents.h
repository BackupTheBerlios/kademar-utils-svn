#ifndef QCOMBOBOXWITHEVENTS_H
#define QCOMBOBOXWITHEVENTS_H

#include <QComboBox>

class QComboBoxWithEvents : public QComboBox
{
    Q_OBJECT
public:
    explicit QComboBoxWithEvents(QWidget *parent = 0);

public slots:
    void readCaption( QString * label );
    void readClicked();

private:
    void enterEvent( QEvent * event );
    void focusInEvent( QFocusEvent * event );

};

#endif // QCOMBOBOXWITHEVENTS_H
