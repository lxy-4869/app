from myFigureCanvas import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout,QWidget
import pandas as pd
from pandas import Series
import shapefile  # 读取shp文件

# 添加图项添加到画布里
from matplotlib.collections import PatchCollection

import seaborn as sns
# 显示中文
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']

import sys
class Main_window(QWidget):#QMainWindow
    def __init__(self):
        super().__init__()
        self.myfigure=QmyFigureCanvas()


        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.myfigure)
        self.setLayout(layout)
        # 设置窗口最小尺寸
        self.setMinimumSize(1090,695)
        # 设置窗口固定尺寸
        self.setFixedSize(self.width(), self.height())

    def draw(self, data_site, data_station):
        city = ['Beijing',
                'Baoding',
                'Cangzhou',
                'Chengde',
                'Handan',
                'Hengshui',
                'Langfang',
                'Qinhuangdao',
                'Shijiazhuang',
                'Tangshan',
                'Xingtai',
                'Zhangjiakou',
                'Tianjin']
        # 县shape文件（不是市文件），不是DataFram，需要通过records()和points()等方法来读取信息
        chn_map2 = shapefile.Reader(r"./map_shp/gadm36_CHN_3.shp")
        date_cmaq=data_site

        colors = sns.color_palette('Paired_r', n_colors=len(city)) # 颜色渐变条
        # 找城市的cmaq数据
        city_shape2 = [x[0] for x in zip(chn_map2.shapes(), chn_map2.records()) if x[1][6] in city] #  通过shapes字段信息来找对应城市的records数据
        city_2 = [x[6] for x in chn_map2.records() if x[6] in city] #  找到该县所在的city，并记录city
        # 分理出经纬度
        site_lon = date_cmaq['lon'].values
        site_lat = date_cmaq['lat'].values

        ## 1
        self.myfigure.figure.clear()  # 清除图表
        ax1 = self.myfigure.figure.add_subplot(1, 3, (1,2) ) # 子图1，占据一行三列的1、2列
        #  根据city来分别画出各自的县地图
        for k in city:
            center_x = []
            center_y = []
            for j, i in zip(city_2, city_shape2):
                if j == k:
                    x, y = zip(*i.points) # 县的地图轮廓经纬度信息，经度x，维度y
                    ax1.plot(x, y, color='#808080', label='fungis')  # #6666ff
                    #  经纬度存在列表里面
                    center_x += list(x)
                    center_y += list(y)
            #  经纬度取均值处显示city名字
            lon = np.mean(Series(center_x))
            lat = np.mean(Series(center_y))
            #ax1.plot(lon, lat, '*')
            #  显示区域名字
            ax1.annotate(k, xy=(lon, lat) )#fontsize=17)

        #显示station
        station=data_station
        ax1.scatter(station['lon'], station['lat'], marker='o',s=10,c='#000000', alpha=1)

        # 上色，给不同的city加上不同的颜色
        for i, j in enumerate(city):
            for info, shape in zip(city_2, city_shape2):
                patches = []
                if info == j:
                    patches.append(Polygon(np.array(shape.points), True))
                    #  下面这个函数是将画好的图添加到画布里面，也就是将上好的色添加到画布里面覆盖在地图上
                    ax1.add_collection(
                        PatchCollection(patches, facecolor=colors[i], edgecolor='k', linewidths=1, zorder=2, alpha=0.4))
        ax1.set_title('站点显示', size=8)
        ax1.axis('equal')
        ## 2，我们预测得到的结果显示
        ##  将画布分为两行三列，在第三的位置作画
        ax2 = self.myfigure.figure.add_subplot(2, 3, 3)  # figsize=(10, 10))
        ##  子图对应颜色取自相同数值范围，用以比较
        vmax=max(date_cmaq['Predict_PM2.5'].max(), date_cmaq['pm25_camq'].max())
        vmin=min(date_cmaq['Predict_PM2.5'].min(), date_cmaq['pm25_camq'].min())
        cmaq1 = date_cmaq['Predict_PM2.5']
        ##  画预测得到的格子点PM2.5数据，颜色深浅表示浓度大小
        ax2.scatter(site_lon, site_lat, c=cmaq1, marker=',', cmap='RdYlGn_r',s=5, alpha=1, vmin=vmin, vmax=vmax)#将数值映射到vmin，vmax范围，保证子图对应颜色规格一致
        ax2.get_xaxis().set_visible(False)
        ##  画站点记录的真实PM2.5浓度
        ax2.scatter(station['lon'], station['lat'], c=station['PM2.5'], marker='o', s=15, cmap='RdYlGn_r', alpha=1,
                    vmin=vmin, vmax=vmax)
        ax2.set_title('Predict_PM2.5/PM10', size=8)
        ax2.axis('equal')
        ## 3，cmaq数据显示，
        ##  将画布分为二行三列，第6个作图
        ax2 = self.myfigure.figure.add_subplot(2, 3, 6)
        cmaq1 = date_cmaq['pm25_camq']
        ax0 = ax2.scatter(site_lon, site_lat, c=cmaq1, marker=',', cmap='RdYlGn_r', s=5, alpha=1, vmin=vmin, vmax=vmax)  # , s=20
        ax2.scatter(station['lon'], station['lat'], c=station['PM2.5'], marker='o', s=15, cmap='RdYlGn_r', alpha=1,
                    vmin=vmin, vmax=vmax)
        ax2.set_title('CMAQ', size=8)
        ax2.axis('equal')

        self.myfigure.figure.tight_layout()  # 紧凑布局
        self.myfigure.figure.subplots_adjust(wspace=0.1, hspace=0.1,right=0.9)  # 调整子图间距，宽度间隙0.1，高度间隙0.1（都是相对于画布的比例）
        l = 0.92
        b = 0.12
        w = 0.015
        h = 1 - 2 * b
        rect = [l, b, w, h]
        cbar_ax = self.myfigure.figure.add_axes(rect)
        self.myfigure.figure.colorbar(ax0, cax=cbar_ax)# 将ax0的渐变在cbar_ax处画出渐变条

        self.myfigure.redraw()   #重画图表，当调整数据后要从新绘制，需要这个函数，不然会图形叠加
        # 保存画出来的图片
        #plt.savefig('1.jpg')


#下面是直接调用上面的类显示结果，这样可以直接在这里显示，而不需要通过其它模块调用，避免麻烦，也便于找问题
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = Main_window()
    station = pd.read_csv(r"D:\lxy\app\66station_2015-12-21.csv")
    cmaq=pd.read_csv(r"D:\lxy\app\test.csv")#读取经过模型预测得到的结果，调用上面的类来显示图像
    main_window.draw(cmaq,station)
    main_window.show()
    app.exec()