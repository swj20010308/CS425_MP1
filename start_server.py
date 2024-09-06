import socket
import subprocess
## need to change server/client socket variable name.
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

        # # Handle the command
        # if command == "PRINT_HELLO":
        #     print("Hello World", flush=True)
        
        #TODO: handle if command is grep, run grep on a file called machine.i.log and return the result to client
         # Handle the command
        if "grep" in command:
            try:
                # Run the grep command on the machine.i.log file
                result = subprocess.check_output(f"{command} machine.i.log", shell=True)
                # Send the grep result back to the client
                client_socket.sendall(result)
            except subprocess.CalledProcessError as e:
                # If grep fails (e.g., no matches), send a failure message
                client_socket.sendall(b"No matching lines found or grep failed.")
        else:
            # Send an error message if the command is not recognized
            client_socket.sendall(b"Unknown command.")

        # Send acknowledgment back to client
        #client_socket.sendall(b"Command received")
        client_socket.close()

if __name__ == "__main__":
    start_server()