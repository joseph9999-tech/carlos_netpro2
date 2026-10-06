# hello_device.py
# Purpose: Confirm you can import the libraries and structure a script

from ncclient import manager
import requests

# 1. Define device connection parameters as a dictionary
device = {
    "host": "sandbox-router",      # placeholder
    "port": 830,                    # NETCONF default port
    "username": "admin",
    "password": "admin",
    "hostkey_verify": False,        # lab only
    "device_params": {"name": "default"}
}

# 2. Print the parameters to confirm structure
print("=== NETCONF Connection Parameters ===")
for key, value in device.items():
    print(f"  {key}: {value}")

# 3. Define a RESTCONF base URL
restconf_base = "https://sandbox-router/restconf/data"
print(f"\n=== RESTCONF Base URL ===")
print(f"  {restconf_base}")

# 4. Print a reminder of the two protocols we're learning
print("\n=== Protocols ===")
print("  NETCONF: port 830, XML, SSH transport")
print("  RESTCONF: port 443, JSON, HTTPS transport")