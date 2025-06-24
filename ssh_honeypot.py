import logging
import socket
import paramiko
import threading
from logging.handlers import RotatingFileHandler

logging_format = logging.Formatter('%(message)s')

SSH_BANNER = "SSH-2.0-MySSHServer_1.0"
host_key = paramiko.RSAKey(filename='navaneeth.key', password='robovitics')

record_logs = logging.getLogger('record_logs')
record_logs.setLevel(logging.INFO)
record_handler = RotatingFileHandler('records.log', maxBytes=2000, backupCount=20)
record_handler.setFormatter(logging_format)
record_logs.addHandler(record_handler)

cred_logs = logging.getLogger('cred_logs')
cred_logs.setLevel(logging.INFO)
cred_handler = RotatingFileHandler('creds.log', maxBytes=2000, backupCount=20)
cred_handler.setFormatter(logging_format)
cred_logs.addHandler(cred_handler)

def emul_shell(channel, client_ip):
    channel.send(b'\r\nrobovitics_project$ ')
    command = b""
    while True:
        char = channel.recv(1)
        if not char:
            break
        channel.send(char)
        command += char
        if char == b'\r':
            command = command.strip()
            response = b""
            if command == b'exit':
                response = b'\nClosing!!\r\n'
                channel.send(response)
                channel.close()
                break
            elif command == b'start':
                response = b'\nstarting\r\n'
                cred_logs.info(f'Command {command.strip()}'+ 'by' +f'{client_ip}')
            elif command == b'restart':
                response = b'\nrestarting\r\n'
                cred_logs.info(f'Command {command.strip()}'+ 'by' +f'{client_ip}')
            elif command == b'ls':
                response = b'\nssh_server\r\n'
                cred_logs.info(f'Command {command.strip()}'+ 'by' +f'{client_ip}')
            elif command == b'robovitics':
                response = b'\nofficial robotics club\r\n'
            else:
                response = b'\nUnknown command '+command+b'\r\n'
                cred_logs.info(f'Command {command.strip()}'+ 'by' +f'{client_ip}')
            channel.send(response)
            channel.send(b'cybersec_project$ ')
            command = b""

class ssh_server(paramiko.ServerInterface):
    def __init__(self, client_ip, inp_username=None, inp_password=None):
        self.event = threading.Event()
        self.client_ip = client_ip
        self.inp_username = inp_username
        self.inp_password = inp_password

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def get_allowed_auths(self, username):
        return "password"

    def check_auth_password(self, username, password):
        record_logs.info(f'Client {self.client_ip} tried to login with' + f'username:{username}'+ f' & password={password}')
        cred_logs.info({self.client_ip},{username},{password})
        if self.inp_username and self.inp_password:
            if username == self.inp_username and password == self.inp_password:
                return paramiko.AUTH_SUCCESSFUL
            return paramiko.AUTH_FAILED
        return paramiko.AUTH_SUCCESSFUL

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

def client_handling(client, add, username, password):
    client_ip = add[0]
    print(f"{client_ip} has connected <3")
    try:
        transport = paramiko.Transport(client)
        transport.local_version = SSH_BANNER
        server = ssh_server(client_ip=client_ip, inp_username=username, inp_password=password)
        transport.add_server_key(host_key)
        transport.start_server(server=server)
        channel = transport.accept(100)
        if channel is None:
            print("No channel opened :(")
            return
        standard_banner = "Welcome to Navaneeth H K's World! \r\n\r\n"
        channel.send(standard_banner.encode())
        emul_shell(channel, client_ip=client_ip)
    except Exception as error:
        print(f"Error: {error}")
    finally:
        try:
            transport.close()
        except Exception as error:
            print(f"Error closing transport: {error}")
        client.close()

def honey(address, port, username, password):
    socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socks.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socks.bind((address, port))
    socks.listen(5)
    print(f"SSH server is listening on {address}:{port}.")
    while True:
        try:
            client, add = socks.accept()
            ssh_honeypot_thread = threading.Thread(target=client_handling, args=(client, add, username, password))
            ssh_honeypot_thread.start()
        except Exception as error:
            print(f"Error accepting connection: {error}")

honey("127.0.0.1", 2666, 'navaneeth', 'robovitics')
