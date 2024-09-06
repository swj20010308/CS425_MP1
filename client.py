import socket
import argparse
#TODO: Use argparse to take arguments for grep, and send those also to server, e.g. grep [option] pattern [file]
def send_grep_command(host, port, grep_command):
    try:
        # Create a socket connection to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        # Send the "GREP" command (or any other command you want)
        client_socket.sendall(grep_command.encode('utf-8'))

        # Receive response from the server
        response = client_socket.recv(1024)
        print(f"Response from {host}: {response.decode('utf-8')}")

        client_socket.close()
    except Exception as e:
        print(f"Failed to connect to {host}: {str(e)}")

if __name__ == "__main__":
    # Set up argparse to handle command-line arguments
    parser = argparse.ArgumentParser(description='Send a grep command to servers')
    
    # Grep options, pattern, and optional file arguments
    parser.add_argument('pattern', help='Pattern to search for using grep')
    parser.add_argument('-i', '--ignore-case', action='store_true', help='Ignore case when searching')
    parser.add_argument('-v', '--invert-match', action='store_true', help='Select non-matching lines')
    parser.add_argument('-n', '--line-number', action='store_true', help='Show line numbers of matches')

    args = parser.parse_args()

    # Construct the grep command based on the provided arguments
    grep_command = f"grep {'-i' if args.ignore_case else ''} {'-v' if args.invert_match else ''} {'-n' if args.line_number else ''} '{args.pattern}'"
    
    # Strip any extra spaces that might have been added if some options are not used
    grep_command = ' '.join(grep_command.split())
    
    # List of server hostnames
    servers = ['illinois.edu', 'example.com', 'another-server.com']
    server_port = 9999  # The same port for all servers

    # Iterate over all servers and send the GREP command
    for server_host in servers:
        send_grep_command(server_host, server_port, grep_command)