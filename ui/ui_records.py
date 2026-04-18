# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'recordsGTFMVF.ui'
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
from PySide6.QtWidgets import (QApplication, QListWidget, QListWidgetItem, QSizePolicy,
    QWidget)

class Ui_record(object):
    def setupUi(self, record):
        if not record.objectName():
            record.setObjectName(u"record")
        record.resize(540, 360)
        record.setMinimumSize(QSize(540, 360))
        record.setMaximumSize(QSize(540, 360))
        self.record_list = QListWidget(record)
        self.record_list.setObjectName(u"record_list")
        self.record_list.setGeometry(QRect(10, 10, 521, 341))

        self.retranslateUi(record)

        QMetaObject.connectSlotsByName(record)
    # setupUi

    def retranslateUi(self, record):
        record.setWindowTitle(QCoreApplication.translate("record", u"Form", None))
    # retranslateUi

