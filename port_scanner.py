import socket
def scan_port(target,port):
    scanner = socket.socket()
    scanner.settimeout(2)

    try:
        scanner.connect((target,port))
        return "OPEN"
    except ConnectionRefusedError:
        return "CLOSED"
    except socket.timeout:
        return "TIMEOUT"
    finally:
        scanner.close()
print("==============================")
print("       PORT SCANNER")
print("==============================")

target = input("Enter Target:").strip()

try:
    start_port = int(input("Enter starting port: "))
    end_port = int(input("Enter ending port: "))

    if start_port <1 or end_port >65535:
        print("Port numbers must be between 1 and 65535.")
        exit()

    if start_port > end_port:
        print("Starting ports must be equal or less than ending port.")
        exit()

except ValueError:
    print("Please enter valid numbers.")
    exit()

print()
print(f"Scanning {target}....")
print(f"Ports: {start_port} to {end_port}")
print()

open_ports = []
timeout_ports = 0

for port in range(start_port, end_port + 1):
    result = scan_port(target, port)

    if port == "OPEN":
        print(f"Port {port} is open")
        open_ports.append(port)

    elif result == "CLOSED":
        print(f"Port {port} is closed")

    elif result == "TIMEOUT":
        print(f"Port {port} timed out")
        timeout_ports += 1

total_ports = end_port - start_port + 1
closed_ports = total_ports - len(open_ports) - timeout_ports
print()
print("------------------------------------------")
print(f"Target: {target}")
print(f"Port Range: {start_port}-{end_port}")
print(f"Ports Scanned: {total_ports}")
print(f"Closed Ports: {closed_ports}")
print(f"Timeout Ports: {timeout_ports}")

if open_ports:
    print("Open ports:")
    for port in open_ports:
        print(f"- {port}")
else:
    print(f"Open Ports: None")

print("------------------------------------------")
print("Scan complete!")