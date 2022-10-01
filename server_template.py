import socket
import threading

from typing import Tuple

SERVER_PORT = 4040
BUFFER_SIZE = 4096
SERVER_IP =  ""

IP_ASDOS = "34.101.92.60"
UDP_ASDOS = 5353

def request_parser(request_message_raw: bytearray, source_address: Tuple[str, int]) -> str:
    # Put your request message decoding logic here.
    # This method return a str.
    # Anda boleh menambahkan helper fungsi/method sebanyak yang Anda butuhkan selama 
    # TIDAK MENGUBAH ATAUPUN MENGHAPUS SPEC (parameter dan return type) YANG DIMINTA.
    pass

def response_parser(response_mesage_raw: bytearray) -> str:
    # Put your request message decoding logic here.
    # This method return a str.
    # Anda boleh menambahkan helper fungsi/method sebanyak yang Anda butuhkan selama 
    # TIDAK MENGUBAH ATAUPUN MENGHAPUS  SPEC (parameter dan return type) YANG DIMINTA.
    pass

def socket_handler(
    sc: socket.socket, inbound_message_raw: bytearray, source_addr: Tuple[str, int]
):
    inbound_message = inbound_message_raw

    print(f"Menerima input dari {source_addr}: {inbound_message}")



def main():
    # Put the rest of your program's logic here (socket etc.). 
    # Pastikan blok socket Anda berada pada fungsi ini.
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sc:
        sc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sc.bind((SERVER_IP, SERVER_PORT))

        print("Server Successfully Started")
        print("Press Ctrl/CMD+C for end the program")

        while True:
            inbound_message_raw, source_addr = sc.recvfrom(BUFFER_SIZE)
            thread_job = threading.Thread(
                target=socket_handler, args=(sc, inbound_message_raw, source_addr)
            )
            thread_job.start()
# DO NOT ERASE THIS PART!
if __name__ == "__main__":
    main() 
