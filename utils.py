from rich.console import Console

console = Console()

def log_info(message):
    console.print(f"[bold cyan]INFO:{message}[/bold cyan]")

def log_warning(message):
    console.print(f"[bold yellow]WARNING:{message}[/bold yellow]")


