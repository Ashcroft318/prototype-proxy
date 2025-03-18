import socket
import threading
from rich.console import Console
from client_handler import handle_client
from utils import log_info

console = Console()

PROXY_HOST = '0.0.0.0'
PROXY_PORT = 8080

def setup_proxy(host, port):
  log_info(f"[bold purple]W.R.A.I.T.H - Proxy tool for privacy. ")
  try:  
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind((host, port))
    proxy_socket.listen(5)
    log_info(f"[bold purple]W.R.A.I.T.H. listening on ({host}:{port})[/bold purple]")
    return proxy_socket
  except Exception as e:
     console.print(f"❌ Error setting up proxy: {e}", style="bold red")
     return None

def run_proxy(proxy_socket):
  try:
        while True:
            log_info("[bold purple]Waiting for a connection...[/bold purple]")
            client_socket, addr = proxy_socket.accept()
            log_info(f"[bold purple]New connection from {addr}[/bold purple]")
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()
  except Exception as e:
        console.print(f"[red]❌ Error starting proxy server: {e}[/red]")

    
