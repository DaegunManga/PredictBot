# 판다스, 넘파이, 맷플롭립, 뷰티풀숲, 플로틀리 라이브러리
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import config 
import xmltodict
import requests

import plotly.io as pi
import plotly.graph_objs as go

# 시계열 예측 라이브러리 
from prophet import Prophet
from prophet.plot import plot_plotly, add_changepoints_to_plot

from datetime import datetime

class Regression2_f :
    def load_data(self) :
        start_day = '20200101'
        decoding_key = config.api_key
        day = datetime.today().strftime('%Y%m%d') #오늘 날짜
        params ={'serviceKey' : decoding_key, 'pageNo' : '1', 'numOfRows' : '10', 'startCreateDt' : start_day , 'endCreateDt' : day }
        xml = requests.get('http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson', params=params)
        xml_dict = xmltodict.parse(xml.text)    
        data = xml_dict['response']['body']['items']['item']
        self.df = pd.DataFrame(data)
        self.df = self.df.astype({'decideCnt' : 'int'})
        L = [] 
        for y in range (0, len(self.df)) : 
            if y == len(self.df)-1 :
                L.append(self.df.iloc[y,2])
                break
            L.append(self.df.iloc[y, 2] - self.df.iloc[y+1, 2])
        self.df['new'] = L

        self.df = self.df.drop([len(self.df)-1])
        self.df['stateDt'] = pd.to_datetime(self.df['stateDt'])
        self.df_korea = self.df 
    
        
    def pred_Prophet (self) :
        df_prophet = self.df_korea.rename(columns={
            'stateDt': 'ds',
            'new': 'y'
        })
        m = Prophet(
            changepoint_prior_scale=0.2, # 디폴트값 = 0.05
            changepoint_range=0.98,      
            yearly_seasonality=True,   
            weekly_seasonality=True,    
            daily_seasonality=True,     
            seasonality_mode='additive' 
        )

        # 공휴일 가져오기
        m.add_country_holidays(country_name='KOR')

        # 모델 학습
        m.fit(df_prophet)

        # 예측 구간
        future = m.make_future_dataframe(periods=7)
        # 예측 분석
        forecast = m.predict(future)

        # 그래프
        fig = plot_plotly(m, forecast)
        pi.write_image(fig, file = './../fig/Prophet_fig.png',format='png',engine='kaleido')
        
        plt.clf()
        # 체인지 포인트 그래프
        fig2 = m.plot(forecast)
        a = add_changepoints_to_plot(fig2.gca(), m, forecast)
        plt.savefig('./../fig/change_point_fig.png')

        plt.clf()
        fig3 = m.plot_components(forecast)
        plt.savefig('./../fig/detail_fig.png')
        self.forecast = forecast

    def return_info (self) :
        return self.forecast[['ds', 'yhat']].tail(7)













