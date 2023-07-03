from flask import Flask, jsonify, render_template, request
import socket
import struct
import re
import threading

app = Flask(__name__)

ce_data = {}
pe_data = {}


def process_packet(packet_data):
    # Unpack the fields from the received data
    unpacked_data = struct.unpack('<i30sqqqqqqqqqqqq', packet_data)

    # Process the unpacked data
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

    trading_symbol_parts = re.findall(r'^([A-Z]+)(\d{2}[A-Z]{3}\d{2})(\d+[A-Z]+)$', trading_symbol)
    if trading_symbol_parts:
        expiry_date = trading_symbol_parts[0][1]  # Extract the first 6 characters
        strike_price = trading_symbol_parts[0][2][:-2]  # Exclude the last two characters
    else:
        expiry_date = None
        strike_price = None

    # Check if the trading symbol is for CE or PE
    if trading_symbol.endswith('CE'):
        # Check if the key already exists in ce_data
        if trading_symbol in ce_data:
            # Update the values for the existing key
            ce_data[trading_symbol].update({
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
                'Type': 'CE'
            })
        else:
            # Add CE data to dictionary
            ce_data[trading_symbol] = {
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
                'Type': 'CE'
            }
    elif trading_symbol.endswith('PE'):
        # Check if the key already exists in pe_data
        if trading_symbol in pe_data:
            # Update the values for the existing key
            pe_data[trading_symbol].update({
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
                'Type': 'PE'
            })
        else:
            # Add PE data to dictionary
            pe_data[trading_symbol] = {
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
                'Type': 'PE'
            }


def fetch_data():
    # Set up the TCP/IP connection
    host = 'localhost'  # Assuming the server is running on the same machine
    port = 8080
    buffer_size = 1024  # Adjust the buffer size as needed

    # Connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.send(b'\x01')

    # Receive and process the data
    packet_size = 130  # Packet size is fixed at 106 bytes
    buffer = b''  # Buffer to accumulate received data

    while True:
        data = client_socket.recv(buffer_size)
        if not data:
            break

        buffer += data

        # Process complete packets in the buffer
        while len(buffer) >= packet_size:
            packet_data = buffer[:packet_size]
            buffer = buffer[packet_size:]

            process_packet(packet_data)

    # Close the connection
    client_socket.close()


def start_fetching_data():
    thread = threading.Thread(target=fetch_data)
    thread.start()


@app.route('/data', methods=['GET'])
def get_data():
    # Retrieve the expiry date input from the user (e.g., '23JUL23')
    expiry_date = request.args.get('expiry_date')

    # Check if expiry date is provided
    if expiry_date:
        # Filter the CE and PE data based on the provided expiry date
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
        # Return all the CE and PE data
        filtered_ce_data = ce_data
        filtered_pe_data = pe_data

    # Return the filtered data as JSON responses
    return jsonify(ce_data=filtered_ce_data, pe_data=filtered_pe_data)


@app.route('/')
def index():
    # Retrieve the expiry date input from the user (e.g., '23JUL23')
    expiry_date = request.args.get('expiry_date')

    # Retrieve the filtered data based on the expiry date
    response = get_data()
    filtered_data = response.json

    return render_template('index.html', options_data=filtered_data)


if __name__ == '__main__':
    start_fetching_data()  # Start fetching data in a separate thread
    app.run(debug=True, port=5000)
