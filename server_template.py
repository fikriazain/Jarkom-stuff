import socket

from typing import Tuple

SERVER_PORT = 4040
BUFFER_SIZE = 4096
SERVER_IP =  ""

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

def main():
    # Put the rest of your program's logic here (socket etc.). 
    # Pastikan blok socket Anda berada pada fungsi ini.
	sc = socket.socket()
	sc.bind((SERVER_IP, SERVER_PORT))
	sc.listen(2)
	while True:
		connection, address = sc.accept()
		print(f"Menerima address: {address}")
		connection.close()

# DO NOT ERASE THIS PART!
if __name__ == "__main__":
    main() 
