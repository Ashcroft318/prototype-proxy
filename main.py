from proxy import setup_proxy,run_proxy
from rich.console import Console



console = Console()

def main():
    
    proxy_socket = setup_proxy('0.0.0.0', 8080)
    if proxy_socket:
        run_proxy(proxy_socket)
    else:
        console.print("[bold red] Proxy setup failed[/bold red]")


if __name__=="__main__":
    main()