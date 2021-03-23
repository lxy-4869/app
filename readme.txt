软件说明：
该软件设计于预测某一或多地点的大气污染物浓度，预测需要两个数据集，
1：一个是训练数据：用以结合待预测站点数据来构造一个逆距离加权PM2.5/PM10变量，以及做线性回归分析，训练数据集必须包括以下变量：'lon','lat','PM2.5/PM10'
2：待预测站点数据：被预测污染物浓度的地点变量数据集，必须包含以下变量：'pm25_camq','pm10_camq','PRES'，'TEMP','DEWP',   'HUMI','IRAIN','NE_Iws','SE_Iws','cbwd','season'
本软件的预测模型是提前训练好的模型，有线性模型、xgboost。界面1进行所需文件的读取，以及结果的保存；界面2是模型预测，是用训练好的模型对待预测地点进行预测。

数据说明：
训练和预测数据里需要有如下变量：
'PRES'(气压),'TEMP'(温度),'DEWP'(露点温度),'HUMI'(湿度),'IRAIN'(降雨量),'pm25_camq'(camq输出PM2.5),'pm10_camq'(camq输出PM10),'cbwd'()
'NE_Iws'(NE累计风向下累计风速的日均值),
'SE_Iws'(SE累计风向下累计风速的日均值),
'lon'(经度),'lat'(纬度),'season'(季节)

文件说明：
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
pandas、numpy、shapefile、matplotlib、math、joblib、copy、sklearn、xgboost、PyQt5、pyinstaller
