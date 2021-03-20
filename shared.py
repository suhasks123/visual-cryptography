from struct import pack, unpack
import json


def send_data(packet, conn):
    packet_json = json.dumps(packet)
    to_send = packet_json.encode('utf-8')

    data_length = pack('>Q', len(to_send))
    conn.sendall(data_length)
    conn.sendall(to_send)

def receive_data(conn):

    # Receiving huge files is done in chunks
    data_length_bin = conn.recv(8)
    (data_length,) = unpack('>Q', data_length_bin)
    data_bin = b''
    while len(data_bin) < data_length:
        to_read = data_length - len(data_bin)
        data_bin += conn.recv(4096 if to_read > 4096 else to_read)

    data_json = data_bin.decode('utf-8')
    data = json.loads(data_json)

    return data
