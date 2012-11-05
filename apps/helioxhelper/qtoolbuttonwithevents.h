#ifndef QTOOLBUTTONWITHEVENTS_H
#define QTOOLBUTTONWITHEVENTS_H

#include <QToolButton>

class QToolButtonWithEvents : public QToolButton
{
    Q_OBJECT
public:
    explicit QToolButtonWithEvents(QWidget *parent = 0);
    void setTextProperty( QString *prop, QString *value);
    //bool isRecommended() const { return m_isRecommended; }
    //void setIsRecommended(bool isRecommended) { m_isRecommended = isRecommended; }
    //void setIsRecommended(const bool &recommended);
    //bool isRecommended();
    //void setListNumber(const int &listNumber);
    void setToolTip(QString &label);
    void showToolTip();
    void setBlockedSignals(int value);


signals:
    //void buttonClicked(const int &m_listNumber);
    void buttonClicked(QString m_property, QString m_propertyValue);

public slots:
    void readCaption( QString * label );
    void buttonClickedFunction();
    void reactivateBlockedSignals();


private:
    void enterEvent(QEvent * event );
    void focusInEvent( QFocusEvent * event );
    QString m_property;
    QString m_propertyValue;
    void setVisualStyle();
    QString bNormal;
    QString bNormalFocused;
    QString bHover;
    //QString bHoverReversed;
    QString bPressed;
    QString toolTipText;
    bool blockedSignals;


//protected:
//    void keyPressEvent(QEvent *event);

protected:
    bool eventFilter(QObject* object,QEvent* event);
};

#endif // QTOOLBUTTONWITHEVENTS_H
