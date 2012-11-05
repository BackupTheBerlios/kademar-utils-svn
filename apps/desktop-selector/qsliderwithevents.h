#ifndef QSLIDERWITHEVENTS_H
#define QSLIDERWITHEVENTS_H

#include <QSlider>

class QSliderWithEvents : public QSlider
{
    Q_OBJECT
public:
    explicit QSliderWithEvents(QWidget *parent = 0);

public slots:
    void readCaption( QString * label );
    void readSlider(int value);

private:
    void enterEvent( QEvent * event );
    void focusInEvent( QFocusEvent * event );

};

#endif // QSLIDERWITHEVENTS_H
