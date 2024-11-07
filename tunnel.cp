import argparse
import os
import subprocess
import sys
from curses_wrapper import MenuSelector
from typing import Dict


SSH_CONFIG_PATH = "C:/Users/Patrick/.ssh/config"


def parse_ssh_config() -> Dict[str, Dict[str, str]]:
    hosts = {}
    current_host = None

    # SSH Config Datei öffnen und lesen
    with open(SSH_CONFIG_PATH, 'r') as file:
        for line in file:
            line = line.strip()

            # Host block erkennen
            if line.startswith("Host "):
                current_host = line.split()[1]
                hosts[current_host] = {'HostName': '', 'User': ''}

            # Hostname block erkennen
            if line.startswith("HostName") and current_host:
                hosts[current_host]['HostName'] = line.split()[1]

            # User block erkennen
            if line.startswith("User") and current_host:
                hosts[current_host]['User'] = line.split()[1]

    return hosts

def parse_host_names(hosts: Dict[str, Dict[str, str]]) -> list[str]:
    host_names = []
    for host in hosts.keys():
        host_names.append(f'{hosts.get(host).get("User")} at {hosts.get(host).get("HostName")}')

    return host_names

def get_host_data(selected_host: str):
    user, hostname = selected_host.split(" at ")
    return user, hostname



def select_host(hosts: Dict[str, Dict[str, str]]) -> str:
    selector = MenuSelector(hosts, prompt="Wählen Sie einen Host aus:")
    selected_host = selector.select()  # Verwendung des MenuSelectors ohne curses direkt
    return selected_host


def establish_ssh_tunnel(port: int, user: str, hostname: str):
    print(f"Establishing SSH tunnel to {hostname} on port {port}...:")
    command = f"ssh -L {port}:{hostname}:{port} {user}@{hostname} -N"
    print(command)
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"SSH tunnel established to {hostname}:{port} as {user}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to establish SSH tunnel: {e}")
        sys.exit(1)


def main():
    # Command-line Argument Parsing
    parser = argparse.ArgumentParser(description="Set up an SSH tunnel.")
    parser.add_argument("--port", type=int, help="Port for the SSH tunnel")
    args = parser.parse_args()

    # SSH Konfiguration einlesen
    hosts = parse_host_names(parse_ssh_config())

    # Host auswählen
    selected_host = select_host(hosts)

    user, hostname = get_host_data(selected_host)

    # Port auswählen (entweder per cmd-Argument oder Eingabe)
    if args.port:
        port = args.port
    else:
        port = int(input("Geben Sie den Port für den SSH Tunnel ein: "))

    # SSH Tunnel aufbauen
    establish_ssh_tunnel(port, user, hostname)


if __name__ == "__main__":
    main()
