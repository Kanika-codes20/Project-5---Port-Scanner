#Port Scanner — Project Notes

## 1. Project Overview

**Project:** Port Scanner  
**Language:** Python  
**Level:** Beginner → Beginner/Intermediate  
**Purpose:** A simple defensive cybersecurity tool that checks a specified range of ports on a target and identifies whether they are open, closed, or timed out.

For testing, I used:

```text
127.0.0.1
```

This is the loopback address, meaning the scanner was tested against my own computer.

I also created a small local server on port `5000` so I could safely test an open port.

---

# 2. What Is a Port?

A **port** is a numbered communication endpoint used by network applications.

Ports range from:

```text
1 – 65535
```

Different services can listen on different ports.

For example, during testing, I created a local server on:

```text
Port 5000
```

My scanner was then able to detect port 5000 as **OPEN**.

A simple analogy:

> An IP address is like the address of a building, while a port is like a particular door inside that building.

---

# 3. The `socket` Module

I started the project with:

```python
import socket
```

`socket` is a built-in Python module that allows programs to communicate over networks.

I used it to create network sockets and attempt connections to different ports.

---

# 4. Creating a Socket

The basic socket object was created using:

```python
scanner = socket.socket()
```

This creates a socket that can be used to attempt a network connection.

---

# 5. Testing a Single Port

The first connection test used:

```python
scanner.connect((target, port))
```

The target and port are provided together as:

```python
(target, port)
```

For example:

```python
scanner.connect(("127.0.0.1", 80))
```

If the connection succeeds, the port is accepting connections.

If the connection is refused, the port is considered closed for this scanner.

---

# 6. `try` and `except`

I used exception handling so that connection errors would not crash the program.

Example:

```python
try:
    scanner.connect((target, port))
except ConnectionRefusedError:
    print("Port is CLOSED")
```

I also learned that different errors can be handled separately.

For example:

```python
except ConnectionRefusedError:
```

handles a refused connection.

And:

```python
except socket.timeout:
```

handles a connection that takes too long to respond.

---

# 7. Closing the Socket

Sockets use system resources, so they should be closed after use.

Initially, I used:

```python
scanner.close()
```

At first this was placed directly in the scanning loop.

Later, after creating the `scan_port()` function, socket cleanup was moved into:

```python
finally:
    scanner.close()
```

`finally` runs regardless of whether the connection succeeds or an exception occurs.

This ensures the socket is properly closed.

---

# 8. Scanning Multiple Ports

I used a `for` loop:

```python
for port in range(start_port, end_port + 1):
```

This allows the program to scan every port between the starting and ending values.

I learned that Python's `range()` does not include its ending value.

For example:

```python
range(1, 6)
```

produces:

```text
1
2
3
4
5
```

Therefore, I used:

```python
range(start_port, end_port + 1)
```

to include the ending port.

---

# 9. Testing an Open Port

To test the scanner safely, I created a local server.

### `server.py`

```python
import socket

server = socket.socket()

server.bind(("127.0.0.1", 5000))

server.listen()

print("Server is listening on port 5000...")

connection, address = server.accept()
```

The server listens on:

```text
127.0.0.1:5000
```

While this server was running, my Port Scanner detected:

```text
Port 5000 is OPEN
```

This allowed me to test the scanner without scanning another person's computer or network.

---

# 10. User Input

The scanner allows the user to enter:

```python
target = input("Enter target: ").strip()
```

The `.strip()` removes unnecessary spaces from the beginning and end of the input.

For the ports, I used:

```python
start_port = int(input("Enter starting port: "))
end_port = int(input("Enter ending port: "))
```

`input()` returns text, so `int()` converts the entered number into an integer.

---

# 11. Timeout

I added a timeout using:

```python
scanner.settimeout(2)
```

This gives the connection attempt a maximum waiting period of two seconds.

Without a timeout, a connection attempt could potentially wait much longer.

The scanner handles timeout errors with:

```python
except socket.timeout:
    return "TIMEOUT"
```

The program therefore distinguishes between:

```text
OPEN
CLOSED
TIMEOUT
```

---

# 12. Tracking Open Ports

Initially, I only counted open ports.

Later, I changed:

```python
open_ports = 0
```

to:

```python
open_ports = []
```

This allowed the program to remember the actual port numbers.

When an open port is found:

```python
open_ports.append(port)
```

For example:

```python
open_ports = [5000, 8080]
```

means ports 5000 and 8080 were detected as open.

---

# 13. Using `len()`

Because `open_ports` is now a list, I use:

```python
len(open_ports)
```

to find the number of open ports.

The total number of ports scanned is calculated with:

```python
total_ports = end_port - start_port + 1
```

Then:

```python
closed_ports = total_ports - len(open_ports) - timeout_ports
```

calculates how many ports were closed.

---

# 14. Looping Through a List

To display each open port separately, I used:

```python
for port in open_ports:
    print(f"- {port}")
```

If:

```python
open_ports = [5000, 8080]
```

the output becomes:

```text
Open Ports:
- 5000
- 8080
```

This was another use of the `for` loop, this time for iterating through a list rather than a range.

---

# 15. Input Validation

I added validation so incorrect input doesn't immediately crash the program.

The port inputs are protected with:

```python
try:
    start_port = int(input("Enter starting port: "))
    end_port = int(input("Enter ending port: "))

except ValueError:
    print("Please enter valid numbers.")
    exit()
```

If the user enters something like:

```text
abc
```

instead of a number, the program handles it gracefully.

---

## Valid Port Range

I also checked that ports are between 1 and 65535:

```python
if start_port < 1 or end_port > 65535:
    print("Port numbers must be between 1 and 65535.")
    exit()
```

---

## Checking Port Order

I also made sure the starting port isn't greater than the ending port:

```python
if start_port > end_port:
    print("Starting port must be less than or equal to ending port.")
    exit()
```

This prevents an invalid scan range.

---

# 16. Functions

One of the biggest improvements was organizing the actual port-checking logic into a function:

```python
def scan_port(target, port):
```

The function receives:

```text
target
port
```

and returns:

```text
OPEN
CLOSED
TIMEOUT
```

The function:

1. Creates a socket.
2. Sets a two-second timeout.
3. Attempts the connection.
4. Handles connection errors.
5. Returns the result.
6. Closes the socket.

The main program then uses:

```python
result = scan_port(target, port)
```

This keeps the scanning logic separate from the user interface and result handling.

---

# 17. `return` vs `print`

I learned an important difference between `print()` and `return`.

`print()` displays something:

```python
print("OPEN")
```

`return` sends a value back to the code that called the function:

```python
return "OPEN"
```

Therefore, the function can return:

```python
"OPEN"
"CLOSED"
"TIMEOUT"
```

and the main program decides what to do with that result.

---

# 18. Final `scan_port()` Function

```python
def scan_port(target, port):
    scanner = socket.socket()
    scanner.settimeout(2)

    try:
        scanner.connect((target, port))
        return "OPEN"

    except ConnectionRefusedError:
        return "CLOSED"

    except socket.timeout:
        return "TIMEOUT"

    finally:
        scanner.close()
```

---

# 19. Final Project Code

```python
import socket

def scan_port(target, port):
    scanner = socket.socket()
    scanner.settimeout(2)

    try:
        scanner.connect((target, port))
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
print()

target = input("Enter target: ").strip()

try:
    start_port = int(input("Enter starting port: "))
    end_port = int(input("Enter ending port: "))

    if start_port < 1 or end_port > 65535:
        print("Port numbers must be between 1 and 65535.")
        exit()

    if start_port > end_port:
        print("Starting port must be less than or equal to ending port.")
        exit()

except ValueError:
    print("Please enter valid numbers.")
    exit()

print()
print(f"Scanning {target}...")
print(f"Ports: {start_port} to {end_port}")
print()

open_ports = []
timeout_ports = 0

for port in range(start_port, end_port + 1):
    result = scan_port(target, port)

    if result == "OPEN":
        print(f"Port {port} is OPEN")
        open_ports.append(port)

    elif result == "CLOSED":
        print(f"Port {port} is CLOSED")

    elif result == "TIMEOUT":
        print(f"Port {port} TIMED OUT")
        timeout_ports += 1

total_ports = end_port - start_port + 1
closed_ports = total_ports - len(open_ports) - timeout_ports

print()
print("------------------------------")
print(f"Target: {target}")
print(f"Port Range: {start_port}-{end_port}")
print(f"Ports Scanned: {total_ports}")
print(f"Closed Ports: {closed_ports}")
print(f"Timeout Ports: {timeout_ports}")

if open_ports:
    print("Open Ports:")

    for port in open_ports:
        print(f"- {port}")
else:
    print("Open Ports: None")

print("------------------------------")
print("Scan complete!")
```

---

# 20. Python Concepts Learned

Through this project, I practiced:

- `import`
- The `socket` module
- Socket creation
- Network connections
- IP addresses and ports
- `try` / `except`
- Specific exceptions
- `finally`
- `return`
- Functions
- Function parameters
- Lists
- `.append()`
- `len()`
- `for` loops
- `range()`
- `if` / `elif` / `else`
- `or`
- `input()`
- `int()`
- `.strip()`
- f-strings
- Counters
- Input validation
- Timeouts
- Resource cleanup

---

# 21. Cybersecurity Concepts Learned

This project helped me understand:

- What network ports are
- How applications listen for network connections
- How a connection attempt can reveal whether a port is accepting connections
- Why timeouts are important in network programs
- How port scanning can be used for security assessment
- Why authorization matters when scanning systems
- How defensive security tools can be built with Python

---

# 22. Testing

I tested the scanner against my own computer using:

```text
127.0.0.1
```

I created a local server on:

```text
127.0.0.1:5000
```

The scanner successfully detected port 5000 as:

```text
OPEN
```

I also tested:

- Closed ports
- Timed-out ports
- Invalid text input
- Invalid port numbers
- Starting port greater than ending port
- Normal scans
- Scanning a single port
- Multiple-port ranges

The project is working correctly.

---

# 23. Project Status

**STATUS: COMPLETE**

The project is intentionally kept at a beginner-to-moderate level.

I do not need to keep adding features just to make the project larger.

The main goal was to learn Python while building a real, understandable cybersecurity project, and that goal has been achieved.

## What I learned most from this project

The most important part wasn't simply creating a port scanner.

I learned how to:

> Break a cybersecurity problem into smaller programming concepts, understand each part, test it safely, and then combine everything into a working tool.

That is the main learning outcome of this project.
