import re
import socket
import threading

from typing import Tuple

SERVER_PORT = 4040
BUFFER_SIZE = 4096
SERVER_IP =  ""

IP_ASDOS = "34.101.92.60"
UDP_ASDOS = 5353

def request_header(req):
    id_0 = int.from_bytes(req[0:2], "big")
    index2 = int.from_bytes(req[2:3], "big")
    index3 = int.from_bytes(req[3:4], "big")
    qr_1 = index2 & 0x80 >> 7
    opcode_2 = index2 & 0x78 >> 3
    aa_3 = index2 & 0x04 >> 2
    tc_4 = index2 & 0x02 >> 1
    rd_5 = index2 & 0x01
    ra_6 = index3 & 0x80 >> 7
    z_7 =  index3 & 0x40 >> 6
    ad_8 = index3 & 0x20 >> 5
    cd_9 = index3 & 0x10 >> 4
    rcode_10 = index3 & 0x08
    qdcount_11 = int.from_bytes(req[4:6], "big")
    ancount_12 = int.from_bytes(req[6:8], "big")
    nscount_13 = int.from_bytes(req[8:10], "big")
    arcount_14 = int.from_bytes(req[10:12], "big")
    header_list = list()
    header_list.extend((id_0, qr_1, opcode_2, aa_3, tc_4, rd_5, ra_6, z_7, ad_8, cd_9, rcode_10, qdcount_11, ancount_12, nscount_13, arcount_14))
    return header_list

def request_question(req: bytearray):
    domain_list = list()
    byte_position = 12
    while req[byte_position] != 0:
        length = req[byte_position]
        domain_part = req[byte_position+1:byte_position+1+length].decode("ASCII")
        domain_list.append(domain_part)
        byte_position += 1 + length

    byte_position += 1
    domain_0 = ".".join(domain_list)

    qtype_1 = int.from_bytes(req[byte_position:byte_position+2], "big")
    qclass_2 = int.from_bytes(req[byte_position+2:byte_position+4], "big")

    question_list = list()
    question_list.extend((domain_0, qtype_1, qclass_2))
    return question_list


def request_parser(request_message_raw: bytearray, source_address: Tuple[str, int]) -> str:
    # Put your request message decoding logic here.
    # This method return a str.
    # Anda boleh menambahkan helper fungsi/method sebanyak yang Anda butuhkan selama 
    # TIDAK MENGUBAH ATAUPUN MENGHAPUS SPEC (parameter dan return type) YANG DIMINTA.
    #Decode dns request message from client to get header, QUestion, and Answer

    header = request_header(request_message_raw)
    question = request_question(request_message_raw)

    message = ""
    message += "=========================================================================\n"
    message += f"[Request from ('{source_address[0]}', {source_address[1]})]\n"
    message += "-------------------------------------------------------------------------\n"
    message += "HEADERS\n"
    message += f"Request ID: {header[0]}\n"
    message += f"QR: {header[1]} | OPCODE: {header[2]} | AA: {header[3]} | TC: {header[4]} | RD: {header[5]} | RA: {header[6]} | AD: {header[8]} | CD: {header[9]} | RCODE: {header[10]}\n"
    message += f"Question Count: {header[11]} | Answer Count: {header[12]} | Authority Count: {header[13]} | Additional Count: {header[14]}\n"
    message += "-------------------------------------------------------------------------\n"
    message += "QUESTION\n"
    message += f"Domain Name: {question[0]} | QTYPE: {question[1]} | QCLASS: {question[2]}\n"
    message += "-------------------------------------------------------------------------\n"

    return message

def response_parser(response_mesage_raw: bytearray) -> str:
    # Put your request message decoding logic here.
    # This method return a str.
    # Anda boleh menambahkan helper fungsi/method sebanyak yang Anda butuhkan selama 
    # TIDAK MENGUBAH ATAUPUN MENGHAPUS  SPEC (parameter dan return type) YANG DIMINTA.

    pass

def socket_handler(
    sc: socket.socket, inbound_message_raw: bytearray, source_addr: Tuple[str, int]
):
    
    #Decode dns request message from client (Headers, Question, Answers only)
    sc.sendto(inbound_message_raw, (IP_ASDOS, UDP_ASDOS))
    reply = sc.recv(512)
    print(reply)



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
            print(request_parser(bytearray(inbound_message_raw), source_addr))
            thread_job = threading.Thread(
                target=socket_handler, args=(sc, inbound_message_raw, source_addr)
            )
            thread_job.start()
# DO NOT ERASE THIS PART!
if __name__ == "__main__":
    main() 
