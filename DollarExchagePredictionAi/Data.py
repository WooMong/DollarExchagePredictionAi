from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# 환율 데이터를 가져오는 함수
def fetch_exchange_rates(base_currency='USD', target_currency='EUR', period='10y'):
    import yfinance as yf
    pair = f'{base_currency}{target_currency}=X'
    data = yf.download(pair, period=period)
    return data
# 데이터 수집 및 CSV 파일로 저장하는 함수
def save_exchange_data(period='10y'):
    exchange_data = fetch_exchange_rates(period=period)

    if not exchange_data.empty:
        exchange_data.reset_index(inplace=True)
        csv_file = f'exchange_rate_data_{period}.csv'  # 파일명에 기간 추가
        exchange_data.to_csv(csv_file, index=False)
        return csv_file
    else:
        return None

# 기본 10년 데이터 저장
save_exchange_data()
# 다양한 기간에 대해 데이터 저장
periods = ['1mo', '6mo', '1y', '5y', '10y']
for period in periods:
    save_exchange_data(period=period)

@app.route('/')
def index():
    return render_template('index.html', periods=periods)

@app.route('/exchange_rate', methods=['POST'])
def exchange_rate():
    period = request.form['period']
    csv_file = f'exchange_rate_data_{period}.csv'
    df = pd.read_csv(csv_file)
    dates = df['Date'].tolist()
    rates = df['Close'].tolist()
    return render_template('exchange_rate.html', dates=dates, rates=rates, period=period)
if __name__ == '__main__':
    app.run(debug=True)
