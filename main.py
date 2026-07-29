import subprocess
from rich import print as cprint
import httpx
import os
import asyncio
import pprint 

logo =  r"""
    ___         __             ____  _                                    
   /   | __  __/ /_____       / __ \(_)___________ _   _____  _______  __ 
  / /| |/ / / / __/ __ \     / / / / ___/ ___/ __ \ | / / _ \/ ___/ / / / 
 / ___ / /_/ / /_/ /_/ /    / /_/ / (__  ) /__/ /_/ / |/ /  __/ /  / /_/ /  
/_/  |_\__,_/\__/\____/    /_____/_/____/\___/\____/|___/\___/_/   \__, /   
                                                                  /____/    
    """



print(logo)



def subFinder():
    domain = input("Enter Domain: ")
    cprint("[bold blue][+][/bold blue][italic bright_yellow] Running Passive Scan [/italic bright_yellow]")
    result = subprocess.run(
            ["subfinder", "-d", domain, "-o", "subdomains.txt"],
            text=True,           
            capture_output=True  
        )
    
    if os.path.exists("subdomains.txt"):
        # print(True)
        subdomains_count = subprocess.check_output(["wc","-l","subdomains.txt"],text=True)
        cprint(f"[bold blue][+][/bold blue] [bold white]{subdomains_count} Subdomains Found ![/bold white]")
    else:
        cprint(f"[bold red][-] Something went wrong ! [/bold red]")


# PASSIVE SCAN..
subFinder()

# --------------------------------------------------------------------------------------------------------------------------------
#use httpx module python version for this and asyncio for reponse delay handling  
print("Starting HTTPX scan...")

# HTTPX
with open("alive.txt", "w") as f:
    subprocess.run([
        "/home/kali/go/bin/httpx",
        "-l",
        "subdomains.txt",
        "-silent"
    ], stdout=f)

print("Alive hosts saved successfully!")

# Read alive hosts
with open("alive.txt") as f:
    hosts = f.readlines()

# FFUF scan
for host in hosts:
    host = host.strip()

    print("Scanning:", host)

    subprocess.run([
        "ffuf",
        "-u",
        f"{host}/FUZZ",
        "-w",
        "/usr/share/wordlists/dirb/common.txt"
    ])
