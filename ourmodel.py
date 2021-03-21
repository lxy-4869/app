import numpy as np
import pandas as pd
from math import asin
import joblib
from copy import deepcopy

class OurModel(object):
    def make_cv(self, target, referencor):
        '''PM25_cv变量的构造'''
        # target: Series 至少要包含(lon,lat)
        # referencor: DataFrame 至少要包含(lon,lat,PM2.5)
        # 先做 radians变成弧度
        x = list(map(np.radians, list(target[['lon', 'lat']])))
        y = referencor[['lon', 'lat']].applymap(np.radians)
        # 变成ndarray
        x = np.array(x)
        y = y.values
        # 弧度距离
        y_x = y - x
        # 弧度变换距离
        a = np.sin(y_x[:, 1] / 2) ** 2 + np.cos(x[1]) * np.cos(y[:, 1]) * np.sin(y_x[:, 0] / 2) ** 2
        distance = list(map(lambda x: x * 2 * 6371 * 1000, list(map(asin, list(np.sqrt(a))))))  # asin，地球直径6371，单位km
        distance = np.round(np.array(distance) / 1000, 4)  # 单位km
        # 逆距离归一化并加权算cv
        ration = distance / distance.sum()
        ration[ration == 0] = np.nan
        cv = (ration * referencor['PM2.5']).sum()
        return (cv)

    def Process(self,Tdata,Pdata):
        ''' xgboost预测PM2.5等操作函数 '''
        #try:
        # 用try、except获取文件处理信息
        data2=deepcopy(Tdata)#被利用的其它站点数据
        data1=deepcopy(Pdata)#带预测站点数据
        #  构造cv变量
        data1['PM25_cv'] = data1.apply(lambda x: self.make_cv(x, data2), axis=1)
        ### 生成dummy变量
        data = self.make_dummy(data1)  # 将处理好的数据放在data里面
        ## <机器学习body
        ### 机器学习的特征
        features = ['PRES', 'TEMP', 'DEWP', 'HUMI', 'IRAIN', 'pm25_camq', 'pm10_camq',
                    'PM25_cv', 'CV_Iws', 'NE_Iws', 'NW_Iws', 'SE_Iws', 'SW_Iws',
                    'lon', 'lat', 'season_1', 'season_2', 'season_3', 'season_4',
                    'cbwd_CV', 'cbwd_NE', 'cbwd_NW', 'cbwd_SE', 'cbwd_SW']

        #高浓度区域线性模型特征
        linxgb_linfeatures=['PM25_cv', 'pm25_camq', 'HUMI','PRES','IRAIN','NW_Iws','SE_Iws',
                            'season_1','season_2','season_3','season_4','cbwd_SE','cbwd_NW', 'cbwd_CV','cbwd_SW', 'cbwd_NE']
        # 高浓度区域相关boost、模型特征
        linxgb_xgbfeatures=['PM25_cv', 'pm25_camq', 'pm10_camq','HUMI', 'TEMP', 'PRES','DEWP','IRAIN','lat',
                            'lon','NW_Iws','cbwd_SE','cbwd_NE']
        # 低浓度区域相关boost、模型特征
        xgb_features=['PM25_cv', 'pm25_camq', 'pm10_camq','HUMI', 'TEMP', 'PRES','lat','lon','cbwd_NW','cbwd_SW']

        ### 读取训练好的模型（这里的三个模型分别是针对高浓度区域10个城市和低浓度区域训练3个城市训练的）
        ### 训练好的模型不需要再次引用相关模块（比如sklearn）
        # 读取gz模型文件
        model_linxgb_lin =joblib.load('./model/model_linxgb_lin.gz')
        model_linxgb_xgb =joblib.load('./model/model_linxgb_xgb.gz')
        model_xgb =joblib.load('./model/model_xgb.gz')
        # 根据class变量将数据分区分为高浓度两块
        high=data[data['class'] == 'high']
        low=data[data['class'] == 'low']

        predict_hight=model_linxgb_xgb.predict(high[linxgb_xgbfeatures])+model_linxgb_lin.predict(high[linxgb_linfeatures])
        predict_low = model_xgb.predict(low[xgb_features])

        data1.loc[data1['class'] == 'high', 'Predict_PM2.5'] = predict_hight
        data1.loc[data1['class'] == 'low', 'Predict_PM2.5'] = predict_low

        self.data = data1
        ## 机器学习body>
        return(data1)


    def make_dummy(self, data):
        '''season、cbwd字符型变量需要做类似one-hot编码'''
        datatemp = data.copy()
        num = datatemp['season'].unique()
        cbwd = datatemp['cbwd'].unique()
        dummies = ['season', 'cbwd']  # 类别变量
        # 将现有的字符做编码
        for dummy in dummies:
            datatemp = datatemp.join(
                pd.get_dummies(datatemp[dummy], prefix=dummy))  # one hot encode:prefix前缀，dummy指定前缀为虚拟化变量的值
        datatemp.drop(['season', 'cbwd'], axis=1, inplace=True)  # 将原变量删掉
        # 有的字符不在里面，getdummy后缺少一些变量，这时候就只能加进去
        season = list(num)
        season4 = list([1, 2, 3, 4])  # season列表
        c = list(set(season4).difference(set(season)))  # 返回列表差集
        cbwd = list(cbwd)
        cbwdall = list(['SW', 'SE', 'NE', 'CV', 'NW'])  # 所有风向列表
        d = list(set(cbwdall).difference(set(cbwd)))  # 返回风向差集
        for i in c:
            datatemp['season_' + str(i)] = 0
        for i in d:
            datatemp['cbwd_' + i] = 0
        return (datatemp)

if __name__=='__main__':
    data1 = pd.read_csv(r"E:\\app\\66station_2015-12-21.csv")
    data2 = pd.read_csv(r"E:\\app\\12787site_2class_2015-12-21.csv")
    print(data2.columns)
    model = OurModel()
    predict=model.Process(data1, data2)
    print(predict.columns)