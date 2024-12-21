# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QSizePolicy,
    QTableView, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(653, 314)
        self.label_w1 = QLabel(Widget)
        self.label_w1.setObjectName(u"label_w1")
        self.label_w1.setGeometry(QRect(20, 10, 191, 31))
        font = QFont()
        font.setPointSize(14)
        self.label_w1.setFont(font)
        self.tableView_w = QTableView(Widget)
        self.tableView_w.setObjectName(u"tableView_w")
        self.tableView_w.setGeometry(QRect(10, 40, 631, 261))

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Weather widget", None))
        self.label_w1.setText(QCoreApplication.translate("Widget", u"City", None))
    # retranslateUi

