# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'acquisition_widgetVIZImg.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
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
from PySide6.QtWidgets import (QApplication, QLabel, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QTextBrowser, QWidget)

class Ui_Acquisition_center(object):
    def setupUi(self, Acquisition_center):
        if not Acquisition_center.objectName():
            Acquisition_center.setObjectName(u"Acquisition_center")
        Acquisition_center.resize(400, 300)
        Acquisition_center.setMinimumSize(QSize(400, 300))
        Acquisition_center.setMaximumSize(QSize(400, 300))
        self.products_list = QListWidget(Acquisition_center)
        self.products_list.setObjectName(u"products_list")
        self.products_list.setGeometry(QRect(15, 21, 301, 261))
        self.acquisition_purchase = QPushButton(Acquisition_center)
        self.acquisition_purchase.setObjectName(u"acquisition_purchase")
        self.acquisition_purchase.setGeometry(QRect(320, 250, 71, 31))
        self.cost_count = QTextBrowser(Acquisition_center)
        self.cost_count.setObjectName(u"cost_count")
        self.cost_count.setGeometry(QRect(320, 50, 71, 31))
        self.label = QLabel(Acquisition_center)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(325, 30, 61, 16))
        self.textBrowser = QTextBrowser(Acquisition_center)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(320, 115, 71, 131))
        self.label_2 = QLabel(Acquisition_center)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(345, 90, 31, 21))

        self.retranslateUi(Acquisition_center)

        QMetaObject.connectSlotsByName(Acquisition_center)
    # setupUi

    def retranslateUi(self, Acquisition_center):
        Acquisition_center.setWindowTitle(QCoreApplication.translate("Acquisition_center", u"Form", None))
        self.acquisition_purchase.setText(QCoreApplication.translate("Acquisition_center", u"\u83b7\u53d6", None))
        self.label.setText(QCoreApplication.translate("Acquisition_center", u"\u5df2\u82b1\u8d39\u91d1\u989d", None))
        self.label_2.setText(QCoreApplication.translate("Acquisition_center", u"\u5185\u5bb9", None))
    # retranslateUi

