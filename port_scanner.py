import socket
import argparse
import threading

def parse_arguments():
    parser = argparse.ArgumentParser(description="Advanced Port Scanner")
    parser.add_argument("host", help="Target host IP address or domain name")
    parser.add_argument("-p", "--ports", type=str, default="1-1024", 
                        help="Port range to scan (e.g., '1-1024' or '80,443,8080')")
    args = parser.parse_args()
    return args.host, args.ports

def scan_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"Port {port}: Open")
        sock.close()
    except socket.error:
        pass

def port_scan(host, ports):
    start_port, end_port = parse_port_range(ports)
    threads = []
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(host, port))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

def parse_port_range(port_range):
    if '-' in port_range:
        start, end = port_range.split('-')
        return int(start), int(end)
    elif ',' in port_range:
        ports = port_range.split(',')
        return [int(port) for port in ports], [int(port) for port in ports]
    else:
        raise ValueError("Invalid port range format. Use 'start-end' or 'port,port,port'")

if __name__ == "__main__":
    host, ports = parse_arguments()
    port_scan(host, ports)
