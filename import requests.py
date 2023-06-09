import requests
import tkinter as tk

# Constantes
PRICE_URL = "https://www.albion-online-data.com/api/v2/stats/prices/"
LOCATION = 'Lymhurst'
QUALITY = 'O'
#name texts: https://github.com/ao-data/ao-bin-dumps/tree/master/formatted
def get_current_prices(item_name):
    url = PRICE_URL + item_name + '.json?&locations=' + LOCATION + "&qualities=" + QUALITY
    response = requests.get(url)
    
    if response.status_code == 200:
        market_prices = response.json()[0]["sell_price_min"]
        return market_prices
    else:
        print(f"Failed to retrieve market data for {item_name} from albion API.")

def update_prices():
    items_of_interest = items_entry.get()
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
    
    price_label["text"] = str(current_price_data)

# Crear la ventana principal
window = tk.Tk()
window.title("Albion Online Market Prices")
window.geometry("400x250")

# Crear etiqueta y entrada de texto para los items de interés
items_label = tk.Label(window, text="Items of Interest (separated by commas):")
items_label.pack()

items_entry = tk.Entry(window, width=40)
items_entry.pack()

# Botón para actualizar los precios
update_button = tk.Button(window, text="Actualizar", command=update_prices)
update_button.pack()

# Etiqueta para mostrar los precios
price_label = tk.Label(window, text="")
price_label.pack()

# Ejecutar el bucle principal de la interfaz gráfica
window.mainloop()
