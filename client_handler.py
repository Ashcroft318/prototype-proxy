from server_connection import establish_connection, process_client_data
from rich.console import Console
from utils import log_info

console = Console()

def handle_client(client_socket):
    try:
        log_info("[bold purple]Client connected. Establishing tunnel...[/bold purple]")
        server_socket= establish_connection()
        process_client_data(client_socket,server_socket)
    except Exception as e:
        console.print(f"[bold red]❌ Error: Failed to connect {e}[/bold red]")

    finally:
        client_socket.close()
        server_socket.close()
        console.print("[yellow]Connection closed.[/yellow]")