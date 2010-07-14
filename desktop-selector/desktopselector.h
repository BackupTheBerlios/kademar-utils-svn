#ifndef DESKTOPSELECTOR_H
#define DESKTOPSELECTOR_H

#include <QMainWindow>

namespace Ui {
    class DesktopSelector;
}

class DesktopSelector : public QMainWindow {
    Q_OBJECT
public:
    DesktopSelector(QWidget *parent = 0);
    ~DesktopSelector();
    void setMaxResolution();
    void removeDesktops();

public slots:
    void startDesktopKde3();
    void startDesktopKde4();
    void startDesktopGnome();
    void startDesktopLxde();
    void startDesktopIcewm();
    void askForShutdown();

protected:
    void changeEvent(QEvent *e);

private:
    Ui::DesktopSelector *ui;
    void setConnects();
};

#endif // DESKTOPSELECTOR_H
