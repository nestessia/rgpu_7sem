import yfinance as yf
from flask import Flask, request, jsonify
import logging


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.route('/convert', methods=['GET', 'POST'])
def convert_currency():
    try:        
        if request.method == 'POST':
            data = request.json
            amount = float(data['amount'])
            from_currency = data['from_currency']
            to_currency = data['to_currency']
        else:
            amount = float(request.args.get('amount'))
            from_currency = request.args.get('from_currency')
            to_currency = request.args.get('to_currency')
        
        ticker = f"{from_currency}{to_currency}=X"
        
        ticker_obj = yf.Ticker(ticker)
        info = ticker_obj.info
        
        rate = info.get('bid') or info.get('ask') or info['previousClose']
        
        converted_amount = amount * rate
        response = {
            'converted_amount': converted_amount,
            'rate': rate,
            'from': from_currency,
            'to': to_currency
        }

        return jsonify(response)
    except Exception as e:
        app.logger.error(f'Ошибка: {str(e)}', exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
