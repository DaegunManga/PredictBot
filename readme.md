# 코로나 관련 정보 예측 디스코드 봇

<div align="center">
<img src="https://img.shields.io/badge/Python-white?style=flat&logo=Python&logoColor=blue"/> 
</div>
<br>

## index
1. [이미지 파일](#fig-파일)

2. [code파일](#code-파일)

3. [디스코드 이용 사례](#3-디스코드-이용-사례)

## fig 파일
#### 1. Linear_fig.png, ploy_fig.png
###### SKlearn을 활용한 선형회귀, 다항회귀 관련 시각화 사진

#### 2. Prophet_fig.png
###### Prophet을 활용한 예측 모델 시각화 사진

#### 3. detail_fig.png
###### Prophet 함수에서 제공하는 함수 이용
###### 추세가 어떻게 되는지를 알려주는 trend, 공휴일 정보를 알려주는 holidays, 주 별 변화를 보여주는 weekly, 연 별 변화를 보여주는 yearly, 일 별 변화를 보여주는 daily와 같은 정보를 제공함.

#### 4. change_point_fig,png
###### 기존의 예측치에서 커다란 이변이 일어났던 기점을 표시한 change_point에 관한 시각화 정보 사진

## code 파일
#### 1. Regression_discord.py 
###### 입력값을 받으면, 예측 모델 실행 후 관련 정보 사진 제공
###### 버튼 1 : Regression_py.py 파일의 sklearn 모듈 사용
###### 버튼 2 : Regression2_py.py 파일의 prophet 모듈 사용

#### 2. Regression2_py.py
###### __init__ 함수 : 코로나 관련 데이터를 API를 이용해서 가져옴.
###### return_info 함수 : 코로나 관련 전체 데이터, 훈련 데이터, 테스트 데이터의 개수를 반환
###### LinearRegressionf 함수 : 선형회귀 실행 후 관련 데이터 시각화 모듈, MAE MSE RMSE Rsquare 등의 평가 지표 점수 반환
###### polyRegressionf 함수 : 다항회귀 실행 후 관련 데이터 시각화 모듈, MAE MSE RMSE Rsquare 등의 평가 지표 점수 반환
###### return_predict 함수 : 선형회귀, 다항회귀의 예측 값 반환

#### 3. Regression_py.py
###### load_data 함수 : 코로나 관련 데이터를 API를 이용해서 가져옴.
###### pred_Prophet 함수 : Prophet 모듈을 이용한 예측 모델 구현
###### return_info 함수 : 예측 모델을 통한 일주일간의 예측치를 반환


## 3. 디스코드 이용 사례

### 1. 예측 명령어 실행
![image](https://user-images.githubusercontent.com/69490709/224373632-cd7417ed-91e3-4c96-a002-1264243cb725.png)

### 2. sklearn을 활용한 선형회귀 사용, [here](#2-regression2_pypy)
![image](https://user-images.githubusercontent.com/69490709/224373692-4dfed40c-12fb-4acc-a626-e50a024e244f.png)

### 3. 각종 지표를 사용한 점수 반환, [here](#2-regression2_pypy)
![image](https://user-images.githubusercontent.com/69490709/224373744-40145e94-e3e3-475d-ad30-7329eb52766d.png)

### 4. sklearn을 활용한 다항회귀 사용, [here](#2-regression2_pypy)
![image](https://user-images.githubusercontent.com/69490709/224373966-103e2541-1849-4e3b-9d56-f0d9a236c6f8.png)

### 5. 각 모델 별 점수 반환, [here](#2-regression2_pypy)
![image](https://user-images.githubusercontent.com/69490709/224374058-f75da1f4-6b9d-4d04-9ad0-b01220dfb992.png)

### 6. prophet을 이용한 학습, [here](#3-regression_pypy)
![image](https://user-images.githubusercontent.com/69490709/224374294-b0849afc-171c-45df-8863-e166f0b68035.png)

### 7. prophet을 이용한 event 및 trend 반환, [here](#3-regression_pypy)
![image](https://user-images.githubusercontent.com/69490709/224374341-4519cb02-22c3-4e6a-8126-601a5883c435.png)

### 8. prophet의 detail (일, 월, 연 별) 반환, [here](#3-regression_pypy)
![image](https://user-images.githubusercontent.com/69490709/224374391-da090e22-e634-4c6b-afef-b6eec733eff0.png)


## 개선할 점
#### 새로고침을 매일 자동으로 하는 기능 구현
###### + 디스코드 봇 관련 파일은 실행되도록 유지하면서, 회귀 모델을 만드는 방법은 없을지 궁금

