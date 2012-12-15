#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
#from PyQt4 import *
from PyQt4.QtCore import *
#from gui1 import Ui_MainWindow


class instalador(QMainWindow):

    def prepareEndPage(self):
        self.ui.WButons_2.setVisible(False)
        self.ui.scrollArea_2.setVisible(False)
        self.connect(self.ui.BExit_2, SIGNAL("clicked()"), self.close)
