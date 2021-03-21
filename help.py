# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'help.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(659, 264)
        self.textBrowser_3 = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser_3.setEnabled(True)
        self.textBrowser_3.setGeometry(QtCore.QRect(10, 20, 631, 231))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.textBrowser_3.setFont(font)
        self.textBrowser_3.setObjectName("textBrowser_3")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.textBrowser_3.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">软件说明：</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">该软件设计于预测某一或多地点的大气污染物浓度，预测需要两个数据集，</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1：一个是训练数据：用以结合待预测站点数据来构造一个逆距离加权PM2.5/PM10变量，以及做线性回归分析，训练数据集必须包括以下变量：\'<span style=\" font-style:italic; color:#ff0000;\">lon</span>\'<span style=\" font-style:italic;\">,</span>\'<span style=\" font-style:italic; color:#ff0000;\">lat</span>\'<span style=\" font-style:italic;\">,</span>\'<span style=\" font-style:italic; color:#ff0000;\">PM2.5/PM10</span>\'</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2：待预测站点数据：被预测污染物浓度的地点变量数据集，必须包含以下变量：<span style=\" font-style:italic;\">\'</span><span style=\" font-style:italic; color:#ff0000;\">pm25_camq</span><span style=\" font-style:italic;\">\',\'</span><span style=\" font-style:italic; color:#ff0000;\">pm10_camq</span><span style=\" font-style:italic;\">\',\'</span><span style=\" font-style:italic; color:#ff0000;\">PRES</span><span style=\" font-style:italic;\">\'，\'</span><span style=\" font-style:italic; color:#ff0000;\">TEMP</span>\',\'<span style=\" font-style:italic; color:#ff0000;\">DEWP</span>\',   \'<span style=\" font-style:italic; color:#ff0000;\">HUMI</span>\',\'<span style=\" font-style:italic; color:#ff0000;\">IRAIN</span>\',\'<span style=\" font-style:italic; color:#ff0000;\">NE_Iws</span>\',\'<span style=\" font-style:italic; color:#ff0000;\">SE_Iws</span>\',\'<span style=\" font-style:italic; color:#ff0000;\">cbwd</span>\',\'<span style=\" font-style:italic; color:#ff0000;\">season</span>\'</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">本软件的预测模型是提前训练好的模型，有线性模型、xgboost。界面1进行所需文件的读取，以及结果的保存；界面2是模型预测，是用训练好的模型对待预测地点进行预测。</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">数据说明：</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">训练和预测数据里需要有如下变量：</p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">\'</span><span style=\" font-style:italic; color:#ff0000;\">PRES</span>\'(气压),<span style=\" font-style:italic;\">\'</span><span style=\" font-style:italic; color:#ff0000;\">TEMP</span>\'(温度),\'<span style=\" font-style:italic; color:#ff0000;\">DEWP</span>\'(露点温度),\'<span style=\" font-style:italic; color:#ff0000;\">HUMI</span>\'(湿度),\'<span style=\" font-style:italic; color:#ff0000;\">IRAIN</span>\'(降雨量),\'<span style=\" font-style:italic; color:#ff0000;\">pm25_camq</span>\'(camq输出PM2.5),\'<span style=\" font-style:italic; color:#ff0000;\">pm10_camq</span>\'(camq输出PM10),\'<span style=\" font-style:italic; color:#ff0000;\">cbwd</span>\'()</p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\'<span style=\" font-style:italic; color:#ff0000;\">NE_Iws</span>\'(NE累计风向下累计风速的日均值),</p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\'<span style=\" font-style:italic; color:#ff0000;\">SE_Iws</span>\'(SE累计风向下累计风速的日均值),</p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\'<span style=\" font-style:italic; color:#ff0000;\">lon</span>\'(经度),\'<span style=\" font-style:italic; color:#ff0000;\">lat</span>\'(纬度),\'<span style=\" font-style:italic; color:#ff0000;\">season</span>\'(季节)</p></body></html>"))