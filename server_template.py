import re
import socket
import threading

from typing import Tuple

SERVER_PORT = 4040
BUFFER_SIZE = 4096
SERVER_IP =  ""

IP_ASDOS = "34.101.92.60"
UDP_ASDOS = 5353
CLIENT_ADDR = tuple()

def request_header(req):
    id_0 = int.from_bytes(req[0:2], "big")
    index2 = req[2]
    index3 = req[3]
    qr_1 = (index2 & 0x80) >> 7
    opcode_2 = (index2 & 0x78) >> 3
    aa_3 = (index2 & 0x04) >> 2
    tc_4 = (index2 & 0x02) >> 1
    rd_5 = (index2 & 0x01)
    ra_6 = (index3 & 0x80) >> 7
    z_7 = (index3 & 0x40) >> 6
    ad_8 = (index3 & 0x20) >> 5
    cd_9 = (index3 & 0x10) >> 4
    rcode_10 = index3 & 0x08
    qdcount_11 = int.from_bytes(req[4:6], "big")
    ancount_12 = int.from_bytes(req[6:8], "big")
    nscount_13 = int.from_bytes(req[8:10], "big")
    arcount_14 = int.from_bytes(req[10:12], "big")
    header_list = list()
    header_list.extend((id_0, qr_1, opcode_2, aa_3, tc_4, rd_5, ra_6, z_7, ad_8, cd_9, rcode_10, qdcount_11, ancount_12,
                        nscount_13, arcount_14))
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
    return question_list, byte_position+4


def request_parser(request_message_raw: bytearray, source_address: Tuple[str, int]) -> str:
    # Put your request message decoding logic here.
    # This method return a str.
    # Anda boleh menambahkan helper fungsi/method sebanyak yang Anda butuhkan selama
    # TIDAK MENGUBAH ATAUPUN MENGHAPUS SPEC (parameter dan return type) YANG DIMINTA.
    #Decode dns request message from client to get header, QUestion, and Answer

    header = request_header(request_message_raw)
    question, pointer = request_question(request_message_raw)

    message = f"""
    =========================================================================\n
    [Request from ('{source_address[0]}', {source_address[1]})]\n
    -------------------------------------------------------------------------\n
    HEADERS\n
    Request ID: {header[0]}\n
    QR: {header[1]} | OPCODE: {header[2]} | AA: {header[3]} | TC: {header[4]} | RD: {header[5]} | RA: {header[6]} | AD: {header[8]} | CD: {header[9]} | RCODE: {header[10]}\n
    Question Count: {header[11]} | Answer Count: {header[12]} | Authority Count: {header[13]} | Additional Count: {header[14]}\n
    -------------------------------------------------------------------------\n
    QUESTION\n
    Domain Name: {question[0]} | QTYPE: {question[1]} | QCLASS: {question[2]}\n
    -------------------------------------------------------------------------\n
    """

    return message

def answer_parser(req: bytearray, pointer):
    answer_list = list()
    offset = int.from_bytes(req[pointer:pointer+2], "big")&0b0011111111111111
    pointer += 2
    while req[pointer] != 0:
        length = req[pointer]
        domain_part = req[pointer+1:pointer+1+length].decode("ASCII")
        answer_list.append(domain_part)
        pointer += 1 + length
    TYPE = int.from_bytes(req[pointer:pointer+2], "big")
    pointer+=2
    CLASS = int.from_bytes(req[pointer:pointer+2], "big")
    pointer+=2
    TTL = int.from_bytes(req[pointer:pointer+4], "big")
    pointer+=4
    RDLENGTH = int.from_bytes(req[pointer:pointer+2], "big")
    pointer+=2
    RDATA = [str(byte) for byte in req[pointer:pointer+RDLENGTH]]
    ADDR = ".".join(RDATA)
    return answer_list, TYPE, CLASS, TTL, RDLENGTH, ADDR

def response_parser(response_message_raw: bytearray) -> str:
    # Put your request message decoding logic here.
    # This method return a str.
    # Anda boleh menambahkan helper fungsi/method sebanyak yang Anda butuhkan selama
    # TIDAK MENGUBAH ATAUPUN MENGHAPUS  SPEC (parameter dan return type) YANG DIMINTA.
    header = request_header(response_message_raw)
    question, pointer = request_question(response_message_raw)
    answer, TYPE, CLASS, TTL, RDLENGTH, ADDR = answer_parser(response_message_raw, pointer)
    response = f"""
    [Response from DNS Server]\n
    -------------------------------------------------------------------------\n
    HEADERS\n
    Request ID: {header[0]}\n
    QR: {header[1]} | OPCODE: {header[2]} | AA: {header[3]} | TC: {header[4]} | RD: {header[5]} | RA: {header[6]} | AD: {header[8]} | CD: {header[9]} | RCODE: {header[10]}\n
    Question Count: {header[11]} | Answer Count: {header[12]} | Authority Count: {header[13]} | Additional Count: {header[14]}\n
    -------------------------------------------------------------------------\n
    QUESTION\n
    Domain Name: {question[0]} | QTYPE: {question[1]} | QCLASS: {question[2]}\n
    -------------------------------------------------------------------------\n
    ANSWER
    TYPE: {TYPE} | CLASS: {CLASS} | TTL: {TTL} | RDLENGTH: {RDLENGTH}
    IP Address: {ADDR} \n
    ==========================================================================\n
    """
    return response
    pass

def socket_handler(
    sc: socket.socket, inbound_message_raw: bytearray, source_addr: Tuple[str, int]
):

    #Decode dns request message from client (Headers, Question, Answers only)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as forward_sc:
        forward_sc.sendto(inbound_message_raw, (IP_ASDOS, UDP_ASDOS))
        dns_response, _ = forward_sc.recvfrom(BUFFER_SIZE)

        print(response_parser(bytearray(dns_response)))

        sc.sendto(dns_response, source_addr)

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