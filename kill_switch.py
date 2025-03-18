from rich.console import Console

console = Console()

def monitor_kill_switch(kill_flag):
    """This is a kill switch that will be implemented in the future for emergency purposes."""
    while not kill_flag.is_set():
        command = input("Enter 'shutdown' to kill the proxy: ").strip().lower()
        if command =="shutdown":
            kill_flag.set()
            console.print("[red]Emergency kill switch activated! shutting down proxy...[/red]")