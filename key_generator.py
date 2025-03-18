import json
from cryptography.fernet import Fernet

key = Fernet.generate_key()

config = {"OBFUSCATION_KEY": key.decode()}

with open("config.json", "w") as file:
    json.dump(config, file, indent=4)
print(f"Generated Key: {key.decode()}")