import requests
import xmltodict
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import config 

from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression #단순 선형 회귀
from sklearn.metrics import mean_absolute_error #MAE
from sklearn.metrics import mean_squared_error #MSE
from sklearn.metrics import r2_score #R_square
from sklearn.linear_model import SGDRegressor # SGD : stochastic Gradient Descent
from sklearn.preprocessing import PolynomialFeatures

class Regression_f () :
    def __init__ (self) :
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

        L = []
        for y in range (0,len(self.df)) :
            L.append(len(self.df) - y)
        self.df['date'] = L


        self.X = self.df.iloc[:,-1].values
        y = self.df.iloc[:,-2].values
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, y, test_size = 0.2) 
        self.X_train = self.X_train.reshape(-1, 1) 
        self.X_test = self.X_test.reshape(-1, 1) 
        self.y_train = self.y_train.reshape(-1, 1) 
        self.y_test = self.y_test.reshape(-1, 1)
    
    def return_info (self) :
        return len(self.X), len(self.X_train), len(self.X_test)

    def LinearRegressionf (self) :

        self.reg = LinearRegression()
        self.reg.fit(self.X_train, self.y_train) 

        y_pred = self.reg.predict(self.X_test)
        plt.clf()
        plt.scatter(self.X_train, self.y_train, color = 'blue') #산점도 표현
        plt.plot(self.X_test, y_pred, color = 'green') #선 그래프 (예측 값 표시)
        plt.title("Corona (Linear Regression)") #제목 
        plt.xlabel('day')
        plt.ylabel('amount')

        plt.savefig('Linear_fig.png')
        return mean_absolute_error(self.y_test, y_pred), mean_squared_error(self.y_test, y_pred), mean_squared_error(self.y_test, y_pred, squared = False), r2_score(self.y_test, y_pred), str(self.reg.score(self.X_test, self.y_test)*100)[0:2] + '점'

    def polyRegressionf (self) :
        self.poly_reg = PolynomialFeatures(degree = 4)
        X_poly = self.poly_reg.fit_transform(self.X_train)
        self.poly_reg.get_feature_names_out()
        self.lin_reg = LinearRegression()
        self.lin_reg.fit(X_poly, self.y_train)

        X_range = np.arange(min(self.X), max(self.X),0.1)
        X_range = X_range.reshape(-1, 1) 

        plt.clf()
        plt.scatter(self.X_train , self.y_train , color = 'blue')
        plt.plot(X_range, self.lin_reg.predict(self.poly_reg.fit_transform(X_range)), color = 'green')
        plt.title('Corona (Polynomial Regression)')
        plt.xlabel('day')
        plt.ylabel('amount')

        X_poly = self.poly_reg.fit_transform(self.X_test)
        self.poly_reg.get_feature_names_out()

        y_pred = self.lin_reg.predict(self.poly_reg.fit_transform(self.X_test))
        a = str(self.lin_reg.score(X_poly, self.y_test)*100)[0:2]

        plt.savefig('poly_fig.png')
        return mean_absolute_error(self.y_test, y_pred), mean_squared_error(self.y_test, y_pred), mean_squared_error(self.y_test, y_pred, squared = False), r2_score(self.y_test, y_pred), a + '점'

    def return_predict (self) :
        return self.reg.predict([[len(self.df)+1]])[0][0], self.lin_reg.predict(self.poly_reg.fit_transform([[len(self.df)+1]]))[0][0]

