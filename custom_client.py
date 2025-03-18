import socket
from obfuscation import obfuscate, deobfuscate
from rich.console import Console

console = Console()

PROXY_HOST = '127.0.0.1'
PROXY_PORT = 8080

def send_obf_request(request:str) -> str:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((PROXY_HOST, PROXY_PORT))

    obf_request= obfuscate(request)
    client_socket.sendall(obf_request)
    console.print(f"[cyan]obfuscated request sent[/cyan]")

    obf_response = client_socket.recv(4096)
    #console.print(f"[yellow]Raw received obfuscated data: {obf_response}[/yellow]")
    client_socket.close()
    
    response = deobfuscate(obf_response)
    return response

if __name__ == "__main__":
    request = "GET http://example.com/ HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n"
    response = send_obf_request(request)
    console.print("[green]Received response:[/green]")
    console.print(response)
