import socket
from colorama import Fore, Back, Style

def server_start(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print()
        print(Back.YELLOW,end="")
        print(Fore.BLACK+"waiting for connection............... ",end="")
        print(Style.RESET_ALL)
        print()
        conn, addr = s.accept()
        with conn:
            print(Fore.RED + ' Connected by: ', end="")
            print(Back.GREEN + str(addr), end="")
            print(Style.RESET_ALL)

            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                print(Back.MAGENTA, end="")
                print(Fore.CYAN+data,end="")
                print(Style.RESET_ALL)

    s.close()
    conn.close()

def requirement():
	host = input("Enter Host: ")
	port = int(input("Enter Port: "))
	if port > 65535:
		print("port number must be less than 65535")
		return requirement()
	return host, port

host, port = requirement()
server_start(host, port)
