import socket
import subprocess
import argparse

def start_server(host='0.0.0.0', port=9999):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        # Receive command from client
        command = client_socket.recv(1024).decode('utf-8')
        print(f"Received command: {command}") 
        
        # Handle the command
        if "grep" in command:
            try:
                # Run the grep command on the machine.i.log file
                result = subprocess.check_output(f"{command} machine.{port}.log", shell=True)
                # Send the grep result back to the client
                client_socket.sendall(result)
            except subprocess.CalledProcessError as _:
                pass
        client_socket.close()

if __name__ == "__main__":
    # Set up argparse to handle command-line arguments for host and port
    parser = argparse.ArgumentParser(description='Start a grep server')
    parser.add_argument('--port', type=int, default=9999, help='Port number for the server')

    args = parser.parse_args()

    start_server(port=args.port)
