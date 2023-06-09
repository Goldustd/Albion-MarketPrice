import requests
from flask import Flask, render_template, request

# Constantes
PRICE_URL = "https://www.albion-online-data.com/api/v2/stats/prices/"
LOCATION = 'Lymhurst'
QUALITY = 'O'

app = Flask(__name__)

def get_current_prices(item_name):
    url = PRICE_URL + item_name + '.json?&locations=' + LOCATION + "&qualities=" + QUALITY
    response = requests.get(url)
    
    if response.status_code == 200:
        market_prices = response.json()[0]["sell_price_min"]
        return market_prices
    else:
        print(f"Failed to retrieve market data for {item_name} from albion API.")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        items_of_interest = request.form['items']
        items_list = [item.strip() for item in items_of_interest.split(",")]
        
        current_price_data = []
        
        for item in items_list:
            market_prices = get_current_prices(item)
            if market_prices is not None:
                item_data = {
                    'Item Name': item,
                    'Current Price': market_prices
                }
                current_price_data.append(item_data)
        
        return render_template('index.html', current_price_data=current_price_data)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
