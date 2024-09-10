import socket
import argparse
import threading

results = []
lock = threading.Lock() 

# Function to send a grep command to the server
def send_grep_command(host, port, grep_command):
    try:
        # Create a socket connection to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        # Send the grep command to the server
        client_socket.sendall(grep_command.encode('utf-8'))

        # Receive response from the server
        response = client_socket.recv(1024)
        
        # Append the result (host, response) to the shared results list
        with lock: 
            results.append(response.decode('utf-8'))

        client_socket.close()
    except Exception as e:
        print(f"Error connecting to {host}:{port} - {e}")

if __name__ == "__main__":
    # Set up argparse to handle command-line arguments
    parser = argparse.ArgumentParser(description='Send a grep command to servers')
    
    # Grep options, pattern, and optional file arguments
    parser.add_argument('flags', nargs='*', help='Optional flags to forward')
    parser.add_argument('pattern', help='Pattern to search for using grep')

    args = parser.parse_args()
    flags = ' '.join(args.flags) if args.flags else ''

    # Construct the grep command based on the provided arguments
    grep_command = f"grep {flags} '{args.pattern}'"
    
    # Strip any extra spaces that might have been added if some options are not used
    grep_command = ' '.join(grep_command.split())
    print(grep_command)
    
    # List of server hostnames with local ports
    servers = [('localhost', 9999), ('localhost', 10000)]
    
    # Create a list to hold all threads
    threads = []

    # Create and start a thread for each server
    for server_host, server_port in servers:
        thread = threading.Thread(target=send_grep_command, args=(server_host, server_port, grep_command))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # After all threads have completed, you can process the results
    print("Results from servers:")
    for response in results:
        print(response)