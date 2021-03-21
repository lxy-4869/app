map_shp里面是shp文件，用来画地图的
model里面是我们训练好的模型
	model_linxgb_lin:高浓度区域预测模型 线性部分
	model_linxgb_xgb:高浓度区域预测模型 xgboost部分
	model_xgb:低浓度区域x预测模型gboost

plotly 、sklearn、xgboost：python plotly函数

draw_map:用来画图的类，里面包括柱状图和气泡图、散点图
myFigureCanvase：是用来辅助画图类，使得画出来的图具备放大缩小功能
ourmodel：用来调用我们训练好的模型并做预测返回结果的类
widget_tab布局.py：是用Qtdesigner设计好的ui文件转换过来的py文件
widget_tab.ui：是用Qtdesigner设计好的ui文件
app业务：是业务类，用来连接前面的所有类，使得组成一个整体。

66station_2015_12_21:是66个站点，在2015-12-21的数据
12787site-2class-2015-12-21:是划分京津冀地区成12787个格子点，并根据格子点所属地被划分成两个class数据，时间是2015-12-21

需要的依赖包如下：
pandas
numpy
shapefile
matplotlib
math
joblib
copy
sklearn
xgboost
PyQt5
pyinstaller