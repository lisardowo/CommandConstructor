# CommandConstructor (not the final name lol)

Terminal tool that helps me to construct commands for tools like `nmap`, `socat`, `tcpdump` and so cause I think they have more flags than active maintainers

## Supported Tools & Scopes

Currently supported modules include:

### 1. Nmap (Network Mapper)
*   **Host Discovery:** ICMP, TCP/UDP Pings, ARP sweeps.
*   **Scan Techniques:** SYN, Connect, NULL, FIN, Xmas, ACK.
*   **Evasion & Spoofing:** Decoys, IP/Port spoofing, packet fragmentation.
*   **Enumeration:** OS Detection, Version intensity, NSE Scripts.
*   **Timing:** T0-T5 templates, minimum packet rates.
*   **Output Formats:** XML, Grepable, Normal.

Working on them: 

### 2. Socat (Multipurpose Relay)
*   **Protocols:** TCP4, TCP6, UDP4, UDP6, UNIX sockets.
*   **Execution:** `EXEC`, `SYSTEM`, `PTY` allocation, `fork`, `setsid`.
*   **Security:** OpenSSL integration for encrypted bind/reverse shells.
*   **Modifiers:** `reuseaddr`, `crnl`, `stderr`, file descriptors.

### 3. Tcpdump (Packet Analyzer)
*   **Interfaces:** Promiscuous mode, interface selection.
*   **BPF Filters:** Source/Dest networks, port filtering, protocol isolation.
*   **Modifiers:** Hex/ASCII output (`-X`), packet truncation (`-s`), timestamp formatting.

### 4. Iptables / Nftables
*   **Chains:** PREROUTING, INPUT, FORWARD, OUTPUT, POSTROUTING.
*   **Targets:** ACCEPT, DROP, REJECT, SNAT, DNAT, MASQUERADE.
*   **Matching:** State tracking (ESTABLISHED, RELATED), MAC addresses, multiport.

### 5. OpenSSL (Cryptography Toolkit)
*   **Generation:** RSA/EC keys, CSR creation, self-signed certificates.
*   **Format Conversion:** PEM, DER, PFX/PKCS12.
*   **Extraction:** Pulling public keys from private keys or certs.

## Installation
No external dependencies are required. The project uses Python's standard `tty` and `termios` libraries for raw mode terminal manipulation.

## Bugs
 
 1. Only shows one flags for the command and each new option selected generates the command again with just that flag
 2. Commands appear repeated
 3. The cursor moves from the input box to other positions 
 4. Deactivate used commands/change
 5. add saved Command Description Seed view 
~~ 6. nmap does not render 2 categories, prolly because it does not fill the whole column~~
 6.1 following up the sixth ticket, the cuantity of categories that are rendered depends on the size of the terminal (tiny terminal renders 2 or so while full size renders all the categories) 
 ~~7. two chars commands are being separated~~

## Setup

```bash
git clone https://github.com/lisardowo/CommandConstructor
cd CommandConstructo
chmod +x main.py
```

```
> IN <command>

    Tipo        Tipo    Tipo
    1)          1)
    2)          2)
    3)          3)


```


> OUT

    Saved                                  Desc

# About mamushi 

Prolly making a repo alone for this one:

bubbletea (golang) inspired framework to create TUIs using the elm architecture. Pretty rough, ugly, work in progress

to run the smol demo

```bash
#on root directory for the project
python -m Mamushi.demo

```

## sum bugs

 1. Quit command is not being recognized
 2. add colors 
 3. Lose of alignment when striking the words
 4. Change seen indices for a dictionary and add times you can repeat a flag in json
 5. This is not entirely a bug but (and maybe cause i didnt went deep enough in that) but when i needed to debug something in bubbletea i had to actually think in how to see debug values ( without counting the debugger itself) because I could not use directly prints because it was dissmissed by the architecture and wont renderize it or only do it when i closed the program and then it would not be helpful so maybe specific print functions that complete interrupt the render of the model and only renderize the asked values but keeping the functionality may be ool