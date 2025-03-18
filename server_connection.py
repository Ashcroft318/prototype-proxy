import socket
from obfuscation import obfuscate, deobfuscate
from rich.console import Console

console = Console()

TARGET_HOST = 'example.com'
TARGET_PORT = 80

def establish_connection():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((TARGET_HOST, TARGET_PORT))
        return server_socket
    except Exception as e:
        console.print(f"[red]Error connecting to target server {TARGET_HOST}: {TARGET_PORT} -{e}[/red]")
        return None

def process_client_data(client_socket, server_socket):
    while True:
        obf_request = client_socket.recv(4096)
        if not obf_request:
            break
        try:
            request = deobfuscate(obf_request)
        except Exception as e:
            console.print(f"[red]Error: deobfuscating client request{e}[/red]")
            break
        
        console.print("[cyan]Deobfuscated client request: [/cyan]")
        console.print(f"[purple]{request}[/purple]")

        try:
            server_socket.sendall(request.encode())
        except Exception as e:
            console.print(f"[red]Error sending request data:{e}[/red]")
            break

        response = server_socket.recv(4096)
        if not response:
            break


        try:
            obf_response = obfuscate(response.decode())
            #console.print(f"[bold blue]🔒 Forwarding encrypted data [/bold blue]")
        except Exception as e:
            console.print(f"[red]Error obfuscating server response:{e}[/red]")
            break
        
        try:
            client_socket.sendall(obf_response)
            console.print("[bold cyan]Sent obfuscated response to client.[/bold cyan]")
        except Exception as e:
            console.print(f"[red]Error sending response to client: {e}[/red]")
            break
