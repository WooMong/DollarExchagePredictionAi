import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt

# CSV 파일 로드할 때 날짜 열을 인덱스로 설정
df = pd.read_csv('exchange_rate_data_10y.csv', parse_dates=['Date'], index_col='Date')

# 데이터의 인덱스를 일일 빈도로  리샘플링하여 결측치 채우기
df = df.resample('D').ffill()

# 로그 변환으로 변동성 증가
df['Log_Close'] = np.log(df['Close'])

# SARIMA 모델 학습 (계절성을 포함)
model = SARIMAX(df['Log_Close'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
model_fit = model.fit(disp=False)

# 예측을 위해 새로운 인덱스 생성 (3개월 예측)
start_date = df.index[-1] + pd.DateOffset(days=1)
end_date = start_date + pd.DateOffset(months=3)
forecast_index = pd.date_range(start=start_date, end=end_date, freq='D')  # 일일 빈도로 생성

# 예측 수행
forecast_log = model_fit.predict(start=len(df), end=len(df) + len(forecast_index) - 1, typ='levels')
forecast_log.index = forecast_index  # 예측 결과에 인덱스 추가
forecast = np.exp(forecast_log)  # 로그 변환을 되돌리기

# 예측 결과를 데이터프레임으로 변환
forecast_df = pd.DataFrame({
    'Date': forecast_index,
    'Forecast': forecast.round(5)  # 소수점 5자리까지 반올림
})

# 예측 결과를 CSV 파일로 저장 (소수점 5자리까지)
forecast_df.to_csv('predicted_exchange_rate.csv', index=False, float_format='%.5f')



print("CSV 파일로 예측된 환율을 저장했습니다.")
