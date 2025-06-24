# Web-Honeypot-project
A unified Python honeypot framework that emulates both SSH and HTTP services to capture unauthorized access attempts. Built using Paramiko and Flask, it logs credentials, commands, and IP addresses for research and educational purposes.

Features
SSH Honeypot:

Simulated shell environment with custom command responses

Logs usernames, passwords, commands, and IPs

Custom SSH banner and multi-threaded support

HTTP Honeypot:

Fake login page served via Flask

Logs login attempts (username, password, IP)

Configurable credentials and port

Command-line Interface:

Easily switch between SSH and HTTP honeypot modes

Customizable port, address, username, and password

