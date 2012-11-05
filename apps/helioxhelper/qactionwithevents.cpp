#include "qactionwithevents.h"

QActionWithEvents::QActionWithEvents(QObject *parent) :
    QAction(parent)
{
    connect(this, SIGNAL(triggered()),
                 this, SLOT(actionClickedFunction()));
    m_property = QString("");
}


void QActionWithEvents::setTextProperty( QString *prop, QString *value)
{
    m_property = QString (*prop);
    m_propertyValue = QString (*value);
}


QString QActionWithEvents::textProperty()
{
    return m_property;
}

QString QActionWithEvents::textPropertyValue()
{
    return m_propertyValue;
}

void QActionWithEvents::actionClickedFunction()
{
    //qDebug() << "signal"; // << m_listNumber;
    emit actionClicked(m_property, m_propertyValue);
}
