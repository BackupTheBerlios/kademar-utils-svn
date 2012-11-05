#ifndef QACTIONWITHEVENTS_H
#define QACTIONWITHEVENTS_H

#include <QAction>

class QActionWithEvents : public QAction
{
    Q_OBJECT
public:
    explicit QActionWithEvents(QObject *parent = 0);
    void setTextProperty( QString *prop, QString *value);
    QString textProperty();
    QString textPropertyValue();
    
signals:
    //void buttonClicked(const int &m_listNumber);
    void actionClicked(QString m_property, QString m_propertyValue);

public slots:
    void actionClickedFunction();

private:
    QString m_property;
    QString m_propertyValue;

};

#endif // QACTIONWITHEVENTS_H
