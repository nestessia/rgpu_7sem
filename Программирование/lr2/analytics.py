import yfinance as yf
from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/analytics', methods=['GET'])
def get_currency_history():
    try:
        currency = request.args.get('currency')
        period = request.args.get('period', '1mo')
        
        # Преобразуем формат тикера
        if '-' in currency:
            from_curr, to_curr = currency.split('-')
            ticker = f"{from_curr}{to_curr}=X"
        else:
            ticker = currency
            
        # Получаем данные
        data = yf.download(ticker, period=period)
        
        if data.empty:
            return jsonify({'error': 'Данные не найдены'}), 404
            
        # Преобразуем данные в формат JSON
        result = {
            'currency': currency,
            'period': period,
            'data': {
                'dates': data.index.strftime('%Y-%m-%d').values.tolist(),
                'prices': {
                    'open': data['Open'].values.tolist(),
                    'high': data['High'].values.tolist(),
                    'low': data['Low'].values.tolist(),
                    'close': data['Close'].values.tolist(),
                    'volume': data['Volume'].values.tolist()
                },
                'statistics': {
                    'average': float(data['Close'].mean()),
                    'min': float(data['Low'].min()),
                    'max': float(data['High'].max()),
                    'start_price': float(data['Open'].iloc[0]),
                    'end_price': float(data['Close'].iloc[-1]),
                    'change_percent': float(((data['Close'].iloc[-1] - data['Open'].iloc[0]) / data['Open'].iloc[0]) * 100)
                }
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        app.logger.error(f'Ошибка: {str(e)}')
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
