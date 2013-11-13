#ifndef QPUSHBUTTONWITHEVENTS_H
#define QPUSHBUTTONWITHEVENTS_H

#include <QPushButton>
#include "QDebug"
class QPushButtonWithEvents : public QPushButton
{
    Q_OBJECT
    //Q_PROPERTY(bool isRecommended WRITE setIsRecommended READ isRecommended)
public:
    explicit QPushButtonWithEvents(QWidget *parent = 0);
    void setTextProperty( QString *prop, QString *value);
    QString textProperty();
    QString textPropertyValue();

    //bool isRecommended() const { return m_isRecommended; }
    //void setIsRecommended(bool isRecommended) { m_isRecommended = isRecommended; }
    //void setIsRecommended(const bool &recommended);
    //bool isRecommended();
    //void setListNumber(const int &listNumber);

signals:
    //void buttonClicked(const int &m_listNumber);
    void buttonClicked(QString m_property, QString m_propertyValue);

public slots:
    void readCaption( QString * label );
    void buttonClickedFunction();
    void setDefaultStyleSheet();


private:
    void enterEvent( QEvent * event );
    void focusInEvent( QFocusEvent * event );
    void focusOutEvent( QFocusEvent * event );
    QString m_property;
    QString m_propertyValue;

//private slots:

};

#endif // QPUSHBUTTONWITHEVENTS_H
