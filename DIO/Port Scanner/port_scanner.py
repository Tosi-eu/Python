import nmap
import json
import os
from tqdm import tqdm
import time

def save_results(results):
    filename = "results.json"

    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            data.append(results)

        with open(filename, 'w') as file:
            json.dump(data, file, indent=2)
    else:
        with open(filename, 'w') as file:
            json.dump([results], file, indent=2)

def scan_types(scanner, method, protocol, parameters):
    try:
        ports = input("Range of ports to scan: ")
        print("Nmap version: ", scanner.nmap_version())
        print(f"Option chose: {method}")
        ip = input("Enter IP address to scan: ")

        # Use tqdm to create a loading bar
        with tqdm(total=int(ports), desc="Scanning") as pbar:
            for port in range(1, int(ports)+1):
                scanner.scan(ip, f"{port}", parameters)
                pbar.update()

        results = {
            "ip": ip,
            "method": method,
            "scan_info": scanner.scaninfo(),
            "ip_status": scanner[ip].state(),
            "protocols": scanner[ip].all_protocols(),
            "open_ports": list(scanner[ip][protocol].keys())
        }
        print(json.dumps(results, indent=2))
        save_results(results)

    except nmap.nmap.PortScannerError:
        print("You aren't with super user privileges!")

if __name__ == '__main__':
    scanner = nmap.PortScanner()

    while True:
        print("  ###### PORT SCANNER ######")
        print("")
        op = int(input("Scanning Operations available: \n  #    1 -->> SYN <<--   # \n  #    2 -->> TCP <<--   # \n  # "
                       "   3 -->> UDP <<--   # \n  #    4 -->> EXIT<<--   # \nChoose an option: "))

        if op == 1:
            method = "SYN"
            scan_types(scanner, method, "tcp", "-v -sS")
        elif op == 2:
            method = "TCP"
            scan_types(scanner, method, "tcp", "-v -sC")
        elif op == 3:
            method = "UDP"
            scan_types(scanner, method, "udp", "-v -sU")
        elif op == 4:
            print("End of scanner!")
            exit(0)
        else:
            print("Invalid Option!")
