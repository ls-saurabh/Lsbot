import socket
import time

def main(): 
    # Create a socket object to connect to the bot
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    
    try:
        # Connect the socket to the bot's IP address and port
        s.connect(("127.0.0.1", 5556))  # Replace with the bot's IP address and port
        print('Connected to bot')
    except Exception as e:
        print('Error connecting to bot:', e)
        return
    
    print("Type '-help' or '-h' for a list of available commands")

    while True:
        data = input("Enter command: ")
        if data.lower() in ["-help", "-h"]:
            print_available_commands()
        else:
            # Send the command to the bot
            send_command(s, data)
            # Receive and print response from the bot
            response = s.recv(1024).decode()
            print("Response from bot:", response)
    
    s.close()

def send_command(sock, command):
    try:
        # Send the command to the bot
        sock.send(command.encode())
        print('Command sent to bot')
    except Exception as e:
        print('Error sending command to bot:', e)

def print_available_commands():
    print("Available commands:")
    print("- execute <command>: Execute a command on the bot")
    print("- help or -h: Display this list of available commands")

if __name__ == "__main__":
    main()