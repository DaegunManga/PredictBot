# 판다스, 넘파이, 맷플롭립, 뷰티풀숲, 플로틀리 라이브러리
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

import plotly.io as pi
import plotly.graph_objs as go

# 시계열 예측 라이브러리 
from prophet import Prophet
from prophet.plot import plot_plotly, add_changepoints_to_plot

class Regression2_f :
    def __init__(self) :
        # 데이터 읽기 
        url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
        df = pd.read_csv(url, error_bad_lines=False)
        df_korea = df[df['location'] == 'South Korea'] # 한국 확진자수 데이터 추출
        df_korea1 = df_korea.T[3:] # 한국 확진자수 데이터프레임 생성
        # 한국의 확진자 시계열 데이터
        df_korea = df_korea.reset_index().rename(columns={'date': 'Date', 'total_cases': 'Confirmed'})
        df_korea['Date'] = pd.to_datetime(df_korea['Date'])
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=df_korea.Date,
                y=df_korea.total_vaccinations
            )
        )
        self.df_korea = df_korea
        
    def pred_Prophet (self) :
        df_prophet = self.df_korea.rename(columns={
            'Date': 'ds',
            'new_cases': 'y'
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
        pi.write_image(fig, file = 'Prophet_fig.png',format='png',engine='kaleido')
        
        plt.clf()
        # 체인지 포인트 그래프
        fig2 = m.plot(forecast)
        a = add_changepoints_to_plot(fig2.gca(), m, forecast)
        plt.savefig('change_point_fig.png')

        plt.clf()
        fig3 = m.plot_components(forecast)
        plt.savefig('detail_fig.png')
        self.forecast = forecast

    def return_info (self) :
        return self.forecast[['ds', 'yhat']].tail(7)













