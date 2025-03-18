import json
import struct
from rich.console import Console
from cryptography.fernet import Fernet

console = Console()

try:
    with open('config.json','r') as f:
        config = json.load(f)
        OBFUSCATION_KEY = config['OBFUSCATION_KEY'].encode()
        #console.print(f"[bold green]🔑 Loaded OBFUSCATION_KEY: {OBFUSCATION_KEY}[/bold green]")
        #console.print(f"🔑 Loaded OBFUSCATION_KEY: {OBFUSCATION_KEY.decode()}", style="yellow")

except (FileNotFoundError, KeyError) as e:
    console.print(f"[red]❌ Error loading key: {e}[/red]")
    exit(1)

cipher = Fernet(OBFUSCATION_KEY)

def obfuscate(data):
    return cipher.encrypt(data.encode())

def deobfuscate(data):
    return cipher.decrypt(data).decode()


def send_data(proxy_socket, data):
    encrypted_data = obfuscate(data)
    length = struct.pack("!I", len(encrypted_data))
    proxy_socket.sendall(length + encrypted_data)
    console.print(f"🔒 Sent obfuscated data: {encrypted_data.hex()}", style="cyan")

def received_data(proxy_socket):
    try:
        length_data = proxy_socket.recv(4)
        if not length_data:
            console.print("[red] Error: No Length data received[/red]")
            return None
    
        length = struct.unpack("!I", length_data)[0]
        console.print(f"Expecting {length} bytes of encrypted data", style="purple")

    #encrypted_data = proxy_socket.recv(length)
        encrypted_data = b""
        while len(encrypted_data)< length:
            chunk = proxy_socket.recv(length - len(encrypted_data))
            if not chunk:
                console.print("[red]Error: Connection closed before full data was received [/red]")
                return None
            encrypted_data += chunk

        console.print(f"🔓 Received obfuscated data (hex): {encrypted_data.hex()}", style="purple")

        if len(encrypted_data) !=length:
            console.print("[red]Error: Expected {length} bytes but got {len(encrypted_data)}[/red]")
            return None
        

        decrypted_data = deobfuscate(encrypted_data)
        console.print(f"🔓 Successfully decrypted data: {decrypted_data}", style ="purple")
        return decrypted_data
    
    except struct.error as e:
        console.print(f"[red]Error:failed to unpack length data: {e}[/red]")
        return None
    except Exception as e:
        console.print(f"[red]Error: Failed to decrypted the data {e}[/red]")
        return None

#test script
if __name__=="__main__":
 test_message = "Hello, this is a test!"
 encrypted = obfuscate(test_message)
 console.print(f"🔒 Encrypted: {encrypted.hex()}", style="cyan")

 decrypted = deobfuscate(encrypted)
 console.print(f"🔓 Decrypted: {decrypted}", style="purple")

 assert test_message == decrypted, "Decryption failed! The keys may not match."



