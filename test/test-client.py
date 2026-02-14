import socket

HOST = "127.0.0.1"
PORT = 5268

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Connected to {HOST}:{PORT}")
        print("Type commands (SET key value / GET key / DEL key)")
        print("Type 'exit' to quit\n")

        while True:
            command = input(">> ")
            if command.lower() == "exit":
                break

            s.sendall((command + "\n").encode())

            response = s.recv(1024).decode().strip()
            print("Server:", response)

if __name__ == "__main__":
    main()
