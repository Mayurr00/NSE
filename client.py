# import socket
# import struct
# import re

# # Set up the TCP/IP connection
# host = 'localhost'  # Assuming the server is running on the same machine
# port = 8080
# buffer_size = 512  # Adjust the buffer size as needed

# ce_data = {}
# pe_data = {}

# # Connect to the server
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect((host, port))

# # Send the initial request indicating readiness
# client_socket.send(b'\x01')

# # Receive and display the data
# packet_size = 130  # Packet size is fixed at 106 bytes
# buffer = b''  # Buffer to accumulate received data

# while True:
#     data = client_socket.recv(buffer_size)
#     if not data:
#         break

#     buffer += data

#     # Process complete packets in the buffer
#     while len(buffer) >= packet_size:
#         packet_data = buffer[:packet_size]
#         buffer = buffer[packet_size:]

#         # Unpack the fields from the received data
#         unpacked_data = struct.unpack('<i30sqqqqqqqqqqqq', packet_data)

#         # Process the unpacked data
#         packet_length = unpacked_data[0]
#         trading_symbol = unpacked_data[1].decode().strip('\x00') if len(unpacked_data) > 1 else None
#         sequence_number = unpacked_data[2] if len(unpacked_data) > 2 else None
#         timestamp = unpacked_data[3] if len(unpacked_data) > 3 else None
#         ltp = unpacked_data[4] / 100 if len(unpacked_data) > 4 else None
#         ltp_quantity = unpacked_data[5] if len(unpacked_data) > 5 else None
#         volume = unpacked_data[6] if len(unpacked_data) > 6 else None
#         bid_price = unpacked_data[7] / 100 if len(unpacked_data) > 7 else None
#         bid_quantity = unpacked_data[8] if len(unpacked_data) > 8 else None
#         ask_price = unpacked_data[9] / 100 if len(unpacked_data) > 9 else None
#         ask_quantity = unpacked_data[10] if len(unpacked_data) > 10 else None
#         open_interest = unpacked_data[11] if len(unpacked_data) > 11 else None
#         prev_close_price = unpacked_data[12] / 100 if len(unpacked_data) > 12 else None

#         # Split strike price and expiry from trading symbol
#         trading_symbol_parts = re.findall(r'^([A-Z]+)(\d{2}[A-Z]{3}\d{2})(\d+[A-Z]+)$', trading_symbol)
#         if trading_symbol_parts:
#                 expiry_date = trading_symbol_parts[0][1]  # Extract the first 6 characters
#                 strike_price = trading_symbol_parts[0][2][:-2]  # Exclude the last two characters
#         else:
#                 expiry_date = None
#                 strike_price = None

#         # Check if the trading symbol is for CE or PE
#         if trading_symbol.endswith('CE'):
#                 # Check if the key already exists in ce_data
#                 if trading_symbol in ce_data:
#                     # Update the values for the existing key
#                     ce_data[trading_symbol].update({
#                         'Expiry Date': expiry_date,
#                         'Strike Price': strike_price,
#                         'LTP': ltp,
#                         'LTQ': ltp_quantity,
#                         'Volume': volume,
#                         'Bid Price': bid_price,
#                         'Bid Quantity': bid_quantity,
#                         'Ask Price': ask_price,
#                         'Ask Quantity': ask_quantity,
#                         'Open Interest': open_interest,
#                         'Timestamp': timestamp,
#                         'Sequence': sequence_number,
#                         'Previous Close Price': prev_close_price,
#                         'Type':'PE'
#                     })
#                 else:
#                     # Add CE data to dictionary
#                     ce_data[trading_symbol] = {
#                         'Expiry Date': expiry_date,
#                         'Strike Price': strike_price,
#                         'LTP': ltp,
#                         'LTQ': ltp_quantity,
#                         'Volume': volume,
#                         'Bid Price': bid_price,
#                         'Bid Quantity': bid_quantity,
#                         'Ask Price': ask_price,
#                         'Ask Quantity': ask_quantity,
#                         'Open Interest': open_interest,
#                         'Timestamp': timestamp,
#                         'Sequence': sequence_number,
#                         'Previous Close Price': prev_close_price,
#                         'Type':'CE'
#                     }
#         elif trading_symbol.endswith('PE'):
#                 # Check if the key already exists in pe_data
#                 if trading_symbol in pe_data:
#                     # Update the values for the existing key
#                     pe_data[trading_symbol].update({                        
#                         'Expiry Date': expiry_date,
#                         'Strike Price': strike_price,
#                         'LTP': ltp,
#                         'LTQ': ltp_quantity,
#                         'Volume': volume,
#                         'Bid Price': bid_price,
#                         'Bid Quantity': bid_quantity,
#                         'Ask Price': ask_price,
#                         'Ask Quantity': ask_quantity,
#                         'Open Interest': open_interest,
#                         'Timestamp': timestamp,
#                         'Sequence': sequence_number,
#                         'Previous Close Price': prev_close_price,
#                         'Type':'PE'
#                     })
#                 else:
#                     # Add PE data to dictionary
#                     pe_data[trading_symbol] = {                       
#                         'Expiry Date': expiry_date,
#                         'Strike Price': strike_price,
#                         'LTP': ltp,
#                         'LTQ': ltp_quantity,
#                         'Volume': volume,
#                         'Bid Price': bid_price,
#                         'Bid Quantity': bid_quantity,
#                         'Ask Price': ask_price,
#                         'Ask Quantity': ask_quantity,
#                         'Open Interest': open_interest,
#                         'Timestamp': timestamp,
#                         'Sequence': sequence_number,
#                         'Previous Close Price': prev_close_price,
#                         'Type':'PE'
#                     }


#     print('CE:', ce_data)
#     print('PE:', pe_data)

#     # import operator

#     # # Sort CE data by strike price in descending order for each expiry date
#     # ce_data_sorted = {}
#     # for symbol, data in ce_data.items():
#     #     expiry_date = data['Expiry Date']
#     #     if expiry_date in ce_data_sorted:
#     #         ce_data_sorted[expiry_date].append(data)
#     #     else:
#     #         ce_data_sorted[expiry_date] = [data]

#     # for expiry_date, data_list in ce_data_sorted.items():
#     #     ce_data_sorted[expiry_date] = sorted(data_list, key=operator.itemgetter('Strike Price'), reverse=True)

#     # # Sort PE data by strike price in descending order for each expiry date
#     # pe_data_sorted = {}
#     # for symbol, data in pe_data.items():
#     #     expiry_date = data['Expiry Date']
#     #     if expiry_date in pe_data_sorted:
#     #         pe_data_sorted[expiry_date].append(data)
#     #     else:
#     #         pe_data_sorted[expiry_date] = [data]

#     # for expiry_date, data_list in pe_data_sorted.items():
#     #     pe_data_sorted[expiry_date] = sorted(data_list, key=operator.itemgetter('Strike Price'), reverse=True)

#     # # Print the sorted data
#     # print('Sorted CE Data:')
#     # for expiry_date, data_list in ce_data_sorted.items():
#     #     print('Expiry Date:', expiry_date)
#     #     for data in data_list:
#     #         print(data)
#     #         print('Sorted PE Data:')
#     #         for expiry_date, data_list in pe_data_sorted.items():
#     #             print('Expiry Date:', expiry_date)
#     #             for data in data_list:
#     #                 print(data)



# # Close the connection
# client_socket.close()


import socket
import struct
import re


# Set up the TCP/IP connection
host = 'localhost'  # Assuming the server is running on the same machine
port = 8080
buffer_size = 1024  # Adjust the buffer size as needed

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Send the initial request indicating readiness
client_socket.send(b'\x01')

# Receive and display the data
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

        # Unpack the fields from the received data
        unpacked_data = struct.unpack('<i30sqqqqqqqqqqqq', packet_data)

        # Process the unpacked data
        packet_length = unpacked_data[0]
        trading_symbol = (unpacked_data[1].decode().rstrip('\x00') if len(unpacked_data) > 1 else None)
        sequence_number = unpacked_data[2] if len(unpacked_data) > 2 else None
        timestamp = (unpacked_data[3] if len(unpacked_data) > 3 else None)
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
        # Process and display the packet data as needed

        print("Trading Symbol:", trading_symbol)
        print("Sequence Number:", sequence_number)
        print("Timestamp:", timestamp)
        print("Last Traded Price (LTP):", ltp)
        print("Last Traded Quantity:", ltp_quantity)
        print("Volume:", volume)
        print("Bid Price:", bid_price)
        print("Bid Quantity:", bid_quantity)
        print("Ask Price:", ask_price)
        print("Ask Quantity:", ask_quantity)
        print("Open Interest (OI):", open_interest)
        print("Previous Close Price:", prev_close_price)
        print('Expiry Date:',expiry_date)
        print('Strike Price:',strike_price)
        print()

# Close the connection
client_socket.close()
