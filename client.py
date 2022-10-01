import socket

SERVER_IP = "35.223.158.134"
SERVER_PORT = 4040

def main():
	sc.socket(socket.AF_INET, socket.SOCK_STREAM)
	sc.connect((SERVER_IP, SERVER_PORT))
	input_value = input("Input: ")
	bytess = input_value.encode("UTF-8")
	sc.send(bytess)
	sc.close()

if __name__ = "__main__":
	main()
