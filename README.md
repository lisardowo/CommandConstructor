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
No external dependencies are required. UnixForge uses Python's standard `tty` and `termios` libraries for raw mode terminal manipulation.

## Bugs

 1. Only shows up to 2 flags for the command
 2. Commands appear repeated
 3. The cursor moves from the input box to other positions 
 4. Deactivate used commands/change
 5. add Comand Desc Seed view 
 6. nmap does not render 2 categories, prolly because it does not fill the whole column
 7. two chars commands are being separated


```bash
git clone [https://github.com/lisardowo/CommandConstructor](https://github.com/lisardowo/CommandConstructor)
cd COMANDCONS
chmod +x main.py
```

```
> IN

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