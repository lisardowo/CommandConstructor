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

```bash
git clone [https://github.com/lisardowo/CommandConstructor](https://github.com/lisardowo/CommandConstructor)
cd unixforge
chmod +x unixforge.py