# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pool_chooseEtHLuh.ui'
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
from PySide6.QtWidgets import (QApplication, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QWidget)

class Ui_Choose_Pool(object):
    def setupUi(self, Choose_Pool):
        if not Choose_Pool.objectName():
            Choose_Pool.setObjectName(u"Choose_Pool")
        Choose_Pool.resize(258, 299)
        self.pool_list = QListWidget(Choose_Pool)
        self.pool_list.setObjectName(u"pool_list")
        self.pool_list.setGeometry(QRect(10, 20, 180, 270))
        self.pool_list.setMinimumSize(QSize(180, 270))
        self.pool_list.setMaximumSize(QSize(180, 270))
        self.select_bottom = QPushButton(Choose_Pool)
        self.select_bottom.setObjectName(u"select_bottom")
        self.select_bottom.setGeometry(QRect(200, 260, 51, 26))

        self.retranslateUi(Choose_Pool)

        QMetaObject.connectSlotsByName(Choose_Pool)
    # setupUi

    def retranslateUi(self, Choose_Pool):
        Choose_Pool.setWindowTitle(QCoreApplication.translate("Choose_Pool", u"Form", None))
        self.select_bottom.setText(QCoreApplication.translate("Choose_Pool", u"\u9009\u62e9", None))
    # retranslateUi

