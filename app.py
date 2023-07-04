from flask import Flask, jsonify, render_template, request
import socket
import struct
import re
import threading

app = Flask(__name__)

ce_data = {}
pe_data = {}
trading_symbol = 0
sequence_number = 0
timestamp = 0
ltp = 0
ltp_quantity = 0
volume = 0
bid_price = 0
bid_quantity = 0
ask_price = 0
ask_quantity = 0
open_interest = 0
prev_close_price = 0


def process_packet(packet_data):
    
    unpacked_data = struct.unpack('<i30sqqqqqqqqqqqq', packet_data)

    
    packet_length = unpacked_data[0]
    trading_symbol = (
        unpacked_data[1].decode().rstrip('\x00') if len(unpacked_data) > 1 else None
    )
    sequence_number = unpacked_data[2] if len(unpacked_data) > 2 else None
    timestamp = unpacked_data[3] if len(unpacked_data) > 3 else None
    ltp = unpacked_data[4] / 100 if len(unpacked_data) > 4 else None
    ltp_quantity = unpacked_data[5] if len(unpacked_data) > 5 else None
    volume = unpacked_data[6] if len(unpacked_data) > 6 else None
    bid_price = unpacked_data[7] / 100 if len(unpacked_data) > 7 else None
    bid_quantity = unpacked_data[8] if len(unpacked_data) > 8 else None
    ask_price = unpacked_data[9] / 100 if len(unpacked_data) > 9 else None
    ask_quantity = unpacked_data[10] if len(unpacked_data) > 10 else None
    open_interest = unpacked_data[11] if len(unpacked_data) > 11 else None
    prev_close_price = unpacked_data[12] / 100 if len(unpacked_data) > 12 else None
    prev_open_interest = unpacked_data[13] if len(unpacked_data) > 13 else None

    trading_symbol_parts = re.findall(r'^([A-Z]+)(\d{2}[A-Z]{3}\d{2})(\d+[A-Z]+)$', trading_symbol)
    if trading_symbol_parts:
        type_stock = trading_symbol_parts[0][0]
        expiry_date = trading_symbol_parts[0][1]  
        strike_price = trading_symbol_parts[0][2][:-2]  
    else:
        expiry_date = None
        strike_price = None

   
    if trading_symbol.endswith('CE'):
        chng_io=open_interest-prev_open_interest
        chng_cp=ltp-prev_close_price
        
        if trading_symbol in ce_data:
           
            ce_data[trading_symbol].update({
                'Stock_Type': type_stock,
                'Expiry Date': expiry_date,
                'Strike Price': strike_price,
                'LTP': ltp,
                'LTQ': ltp_quantity,
                'Volume': volume,
                'Bid Price': bid_price,
                'Bid Quantity': bid_quantity,
                'Ask Price': ask_price,
                'Ask Quantity': ask_quantity,
                'Open Interest': open_interest,
                'Timestamp': timestamp,
                'Sequence': sequence_number,
                'Previous Close Price': prev_close_price,
                'Previous Open Interest':prev_open_interest,
                'Change OI': chng_io,
                'Change wrt CP': chng_cp,
                'Type': 'CE'
            })
        else:
            
            ce_data[trading_symbol] = {
                'Stock_Type': type_stock,
                'Expiry Date': expiry_date,
                'Strike Price': strike_price,
                'LTP': ltp,
                'LTQ': ltp_quantity,
                'Volume': volume,
                'Bid Price': bid_price,
                'Bid Quantity': bid_quantity,
                'Ask Price': ask_price,
                'Ask Quantity': ask_quantity,
                'Open Interest': open_interest,
                'Timestamp': timestamp,
                'Sequence': sequence_number,
                'Previous Close Price': prev_close_price,
                'Previous Open Interest':prev_open_interest,
                'Change OI': chng_io,
                'Change wrt CP': chng_cp,
                'Type': 'CE'
            }
    elif trading_symbol.endswith('PE'):
        chng_io=open_interest-prev_open_interest
        chng_cp=ltp-prev_close_price
        
        if trading_symbol in pe_data:
            
            pe_data[trading_symbol].update({
                'Stock_Type': type_stock,
                'Expiry Date': expiry_date,
                'Strike Price': strike_price,
                'LTP': ltp,
                'LTQ': ltp_quantity,
                'Volume': volume,
                'Bid Price': bid_price,
                'Bid Quantity': bid_quantity,
                'Ask Price': ask_price,
                'Ask Quantity': ask_quantity,
                'Open Interest': open_interest,
                'Timestamp': timestamp,
                'Sequence': sequence_number,
                'Previous Close Price': prev_close_price,
                'Previous Open Interest':prev_open_interest,
                'Change OI': chng_io,
                'Change wrt CP': chng_cp,
                'Type': 'PE'
            })
        else:
           
            pe_data[trading_symbol] = {
                'Stock_Type': type_stock,
                'Expiry Date': expiry_date,
                'Strike Price': strike_price,
                'LTP': ltp,
                'LTQ': ltp_quantity,
                'Volume': volume,
                'Bid Price': bid_price,
                'Bid Quantity': bid_quantity,
                'Ask Price': ask_price,
                'Ask Quantity': ask_quantity,
                'Open Interest': open_interest,
                'Timestamp': timestamp,
                'Sequence': sequence_number,
                'Previous Close Price': prev_close_price,
                'Previous Open Interest':prev_open_interest,
                'Change OI': chng_io,
                'Change wrt CP': chng_cp,
                'Type': 'PE'
            }


def fetch_data():
    
    host = 'localhost'  
    port = 8080
    buffer_size = 1024  

   
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.send(b'\x01')

   
    packet_size = 130  
    buffer = b''  

    while True:
        data = client_socket.recv(buffer_size)
        if not data:
            break

        buffer += data

       
        while len(buffer) >= packet_size:
            packet_data = buffer[:packet_size]
            buffer = buffer[packet_size:]

            process_packet(packet_data)

    
    client_socket.close()


def start_fetching_data():
    thread = threading.Thread(target=fetch_data)
    thread.start()




@app.route('/data', methods=['GET'])
def get_data():
   
    expiry_date = request.args.get('expiry_date')
    strike_price_range = request.args.get('strike_price_range')
    option_type = request.args.get('option_type')

    
    filtered_ce_data = {}
    filtered_pe_data = {}

    if expiry_date:
        filtered_ce_data = {
            symbol: data
            for symbol, data in ce_data.items()
            if data.get('Expiry Date') == expiry_date
        }
        filtered_pe_data = {
            symbol: data
            for symbol, data in pe_data.items()
            if data.get('Expiry Date') == expiry_date
        }
    else:
        filtered_ce_data = ce_data
        filtered_pe_data = pe_data

    if strike_price_range:
       
        min_strike_price, max_strike_price = strike_price_range.split('-')
        min_strike_price = int(min_strike_price.strip())
        max_strike_price = int(max_strike_price.strip())

        
        filtered_ce_data = {
            symbol: data
            for symbol, data in filtered_ce_data.items()
            if min_strike_price <= int(data.get('Strike Price')) <= max_strike_price
        }
        filtered_pe_data = {
            symbol: data
            for symbol, data in filtered_pe_data.items()
            if min_strike_price <= int(data.get('Strike Price')) <= max_strike_price
        }

   
    if option_type:
        filtered_ce_data = {
            symbol: data
            for symbol, data in filtered_ce_data.items()
            if data.get('Stock_Type') == option_type
        }
        filtered_pe_data = {
            symbol: data
            for symbol, data in filtered_pe_data.items()
            if data.get('Stock_Type') == option_type
        }

   
    return jsonify(ce_data=filtered_ce_data, pe_data=filtered_pe_data)



@app.route('/')
def index():
    
    expiry_date = request.args.get('expiry_date')
    strike_price_range = request.args.get('strike_price_range')

    
    response = get_data()
    filtered_data = response.json

    
    ce_strike_prices = sorted(
        set(int(data['Strike Price']) for data in filtered_data['ce_data'].values())
    )
    pe_strike_prices = sorted(
        set(int(data['Strike Price']) for data in filtered_data['pe_data'].values())
    )

    
    min_strike_price = 35000
    max_strike_price = 50000
    increment = 50
    strike_prices = list(range(min_strike_price, max_strike_price + increment, increment))

    
    strike_prices = [price for price in strike_prices if price >= min(ce_strike_prices + pe_strike_prices)]

    return render_template('index.html', options_data=filtered_data,
                           expiry_date=expiry_date, strike_price_range=strike_price_range,
                           strike_prices=strike_prices)


# ...

if __name__ == '__main__':
    start_fetching_data()  
    app.run(debug=True, port=5000)
