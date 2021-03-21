#PyQt5部分
import sys
from PyQt5.QtWidgets import QApplication,QFileDialog,QMessageBox,QWidget
from widget_tab import *
from ourmodel import OurModel #我们的预测模型，封装成了类
from draw_map import *
from help import *
import image

#数据处理部分
import pandas as pd
import numpy as np


class App(QWidget):

    def __init__(self,parent=None):
        # 文件变量赋值
        self.fileName_1=''
        self.fileName_2=''
        self.fileName_3=''
        self.aera=''
        super().__init__(parent)
        self.ui = Ui_Form()  # 创建UI对象
        self.ui.setupUi(self)  # 构造UI界面
        self.initUi()
    def initUi(self):
        '丰富界面内容，给界面添加事件'
        # 页面1
        self.ui.pushButton_6.clicked.connect(self.getdatafile)
        self.ui.pushButton_7.clicked.connect(self.getdatafile)
        self.ui.pushButton_8.clicked.connect(self.savefile)
        self.ui.pushButton_3.clicked.connect(self.help)

        #页面2
        self.ui.pushButton.clicked.connect(self.process)
        self.ui.pushButton_2.clicked.connect(self.site_map)
        self.ui.pushButton_4.clicked.connect(self.process)



        self.map_window = Main_window()

    # 文件读写函数
    def getdatafile(self):
        '''读文件'''
        buttonmessage=self.sender()
        if buttonmessage.text()=='导入训练数据文件':
            self.fileName_1, filetype1 = QFileDialog.getOpenFileName(self, "选取文件", "./",
                                                                     "All Files (*.csv)")  # 设置文件扩展名过滤,注意用双分号间隔
            self.ui.lineEdit_5.setText(self.fileName_1)
            if self.fileName_1 !='':
                self.data1 = pd.read_csv(self.fileName_1)
        else:
            self.fileName_2, filetype2 = QFileDialog.getOpenFileName(self, "选取文件", "./",
                                                                    "All Files (*.csv)")  # 设置文件扩展名过滤,注意用双分号间隔
            self.ui.lineEdit_6.setText(self.fileName_2)
            if self.fileName_2 !='':
                self.data2 = pd.read_csv(self.fileName_2)

    def savefile(self):
        '''保存文件'''
        self.fileName_3, ok2 = QFileDialog.getSaveFileName(self, "文件保存", "./",
                                                          "All Files (*);;Text Files (*.csv)")  # 指定了要保存的文件类型
        self.ui.lineEdit_7.setText(self.fileName_3)

    # 处理数据及赋予控件实际作用函数
    def process(self):
        sender = self.sender()
        print(sender.text())
        try:
            model=OurModel()
            self.data_3model=model.Process(self.data1,self.data2)
            self.data_3model.to_csv(self.fileName_3)
            Printdata = str(self.data_3model[['lon', 'lat', 'city', 'Predict_PM2.5']])
            QMessageBox.about(self, '反馈信息', '预测完成！！')
            if self.ui.textBrowser.toPlainText()!=None:
                self.ui.textBrowser.clear()
            self.ui.textBrowser.setText(Printdata)
            self.draw(sender.text())

        except:
            if self.fileName_1 == '':
                QMessageBox.warning(self, '反馈信息', '请输入训练文件！！')
            elif self.fileName_2 == '':
                QMessageBox.warning(self, '反馈信息', '请输入待预测文件！！')
            elif self.fileName_3 == '':
                QMessageBox.warning(self, '反馈信息', '请输入保存文件地址！！')
            else:
                QMessageBox.warning(self, '反馈信息', '文件处理出错！！')  # 内部函数问题'''

    def draw(self, sender):
        data_3model_temp=self.data_3model.groupby('city', as_index=False).mean()
        data_3model_lon = data_3model_temp['lon']
        data_3model_lat = data_3model_temp['lat']
        data_3model_station = data_3model_temp['city']
        data_3model_data_PM25 = data_3model_temp['Predict_PM2.5']
        self.barfigure(data_3model_station, data_3model_data_PM25 , sender)
        self.bubblefigure(data_3model_lon, data_3model_lat, data_3model_data_PM25, data_3model_station, sender)
        self.compare_camq(self.data_3model['Predict_PM2.5'], self.data_3model['pm25_camq'], sender)

    # 绘图函数
    def barfigure(self, station, PM25, sender):
        self.ui.tab_3.figure.clear()  # 清除图表
        ax1 = self.ui.tab_3.figure.add_subplot(1, 1, 1)
        x = station
        y = PM25
        width = 0.5 # bar之间的间隔
        ylength = y.max() - y.min() # y的长度
        ax1.barh(range(len(x)), y, width) #, align="center")
        ax1.set_yticks(range(len(x)))
        fontsize=round(len(station)/11*6, 1) # 控制label字体大小
        textfontsize = round(len(station) / 11 * 7, 1)
        ax1.set_yticklabels(x, fontsize=fontsize, rotation=0)
        ax1.set_xlabel('PM2.5')
        for i, j, z in zip(y, range(len(x)), y):
            ax1.annotate('%.3f' % z, xy=(i-ylength/10, j+width), fontsize=textfontsize, va='top')
        self.ui.tab_3.redraw()  # 重画图表

    def bubblefigure(self,lon,lat,data,station, sender):
        self.ui.tab_4.figure.clear()  # 清除图表
        ax1 = self.ui.tab_4.figure.add_subplot(1, 1, 1)
        lon = lon
        lat = lat

        #对数据做尺度变化和位置变化，变到100-2000，便于做气泡图时正常显示
        data2 = data
        datamin=data2.min()
        datamax=data2.max()
        scale=[100,2000]
        data2=(data2-datamin)*(scale[1]-scale[0])/(datamax-datamin)+scale[0]
        lonstep=(lon.max()-lon.min())/5
        lonlist=np.arange(lon.min(),lon.max()+lonstep,lonstep)
        latstep=(lat.max()-lat.min())/5
        latlist=np.arange(lat.min(),lat.max()+latstep,latstep)

        sc =ax1.scatter(np.array(lon), np.array(lat), np.array(data2),#当明确指定参数s时不能设置形状大小，很奇怪
                marker="o", c=data,
                vmin=data.min(), vmax=data.max(),
                cmap='RdYlGn_r',#颜色范围
                alpha=0.8)    #透明度

        ax1.set_xticks(lonlist)
        ax1.set_yticks(latlist)
        ax1.tick_params(axis='both', which='major', labelsize=7)

        for i, j, z in zip(lon, lat, station):
            ax1.annotate(z,xy=(i-lonstep/10 ,j), fontsize=7)

        ax1.set_xlabel('lon')
        ax1.set_ylabel('lat')
        self.ui.tab_4.figure.colorbar(sc)  # 能加渐变条
        self.ui.tab_4.redraw()  # 重画图表


    def compare_camq(self, Predict_PM25, PM25_camq, sender):
        self.ui.tab_6.figure.clear()  # 清除图表
        ax1 = self.ui.tab_6.figure.add_subplot(1, 1, 1)

        ax1.scatter(Predict_PM25,PM25_camq,s=3)
        length=max(Predict_PM25.max(),PM25_camq.max())
        step=length/10
        ax1.set_xticks(np.arange(0, length+step, step))
        ax1.set_yticks(np.arange(0, length+step, step))
        ax1.set_xlabel('Predict_Pm25')
        ax1.set_ylabel('Pm25_camq')
        ax1.plot(np.arange(0, length, step/10),np.arange(0, length, step/10))
        self.ui.tab_6.redraw()  # 重画图表


    def site_map(self):
        self.map_window.draw(self.data_3model, self.data1)
        self.map_window.show()


    def help(self):
        self.form2 = QtWidgets.QWidget()
        self.ui2 = Ui_Dialog()
        self.ui2.setupUi(self.form2)
        self.form2.show()



if __name__=='__main__':
    app=QApplication(sys.argv)
    myapp=App()
    myapp.show()
    sys.exit(app.exec())