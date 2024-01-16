import nmap

if __name__ == '__main__':
    scanner = nmap.PortScanner()

    while True:
        print("###### PORT SCANNER ######")
        print("")
        op = int(input("Scanning Operations available: \n  #    1 -->> SYN <<--   # \n  #    2 -->> TCP <<--   # \n  # "
                       "   3 -->> UDP <<--   # \n  #    4 -->> TCP NULL"
                       "<<-#\n  #    5 -->> EXIT"))

        if op==1:
            try:
                ports = input("Range of ports to scan: ")
                print("Nmap version: ", scanner.nmap_version())
                print("Option chose: SYN")
                ip = input("Enter IP address to scan: ")
                scanner.scan(ip, f"1-{ports}", "-v -sS") #SYN
                print(scanner.scaninfo())
                print("IP Status: ", scanner[ip].state())
                print("Protocols available: ", scanner[ip].all_protocols())
                print("")
                print("Open ports: ", scanner[ip]['tcp'].keys())
            except nmap.nmap.PortScannerError:
                print("You aren't with super user privileges!")
        elif op==2:
            try:
                ports = input("Range of ports to scan: ")
                print("Nmap version: ", scanner.nmap_version())
                print("Option chose: TCP")
                ip = input("Enter IP address to scan: ")
                scanner.scan(ip, f"1-{ports}", "-v -sC") #TCP
                print(scanner.scaninfo())
                print("IP Status: ", scanner[ip].state())
                print("Protocols available: ", scanner[ip].all_protocols())
                print("")
                print("Open ports: ", scanner[ip]['tcp'].keys())
            except nmap.nmap.PortScannerError:
                print("You aren't with super user privileges!")
        elif op==3:
            try:
                ports = input("Range of ports to scan: ")
                print("Nmap version: ", scanner.nmap_version())
                print("Option chose: UDP")
                ip = input("Enter IP address to scan: ")
                scanner.scan(ip, f"1-{ports}", "-v -sU") #UDP
                print(scanner.scaninfo())
                print("IP Status: ", scanner[ip].state())
                print("Protocols available: ", scanner[ip].all_protocols())
                print("")
                print("Open ports: ", scanner[ip]['udp'].keys())
            except nmap.nmap.PortScannerError:
                print("You aren't with super user privileges!")
        elif op==4:
            try:
                ports = input("Range of ports to scan: ")
                print("Nmap version: ", scanner.nmap_version())
                print("Option chose: TCP NULL")
                ip = input("Enter IP address to scan: ")
                scanner.scan(ip, f"1-{ports}", "-v -sN") #TCP NULL
                print(scanner.scaninfo())
                print("IP Status: ", scanner[ip].state())
                print("Protocols available: ", scanner[ip].all_protocols())
                print("")
                print("Open ports: ", scanner[ip]['tcp'].keys())
            except nmap.nmap.PortScannerError:
                print("You aren't with super user privileges!")
        elif op==5:
            print("End of scanner!")
            exit(0)
        else:
            print("Invalid Option!")


