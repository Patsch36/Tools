import subprocess
import os
import argparse
import re
import curses  # install with windows-curses on mac, leave on linux
from tools.curses_wrapper import MenuSelector

SSH_CONFIG_PATH = os.path.expanduser("~/.ssh/config")


def parse_ssh_config():
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


def choose_host_or_ip():
    hosts = parse_ssh_config()
    host_list = list(hosts.keys())

    selector = MenuSelector(
        sorted(host_list), prompt="Select a host or enter an IP:")
    selected_host = selector.select()

    if selected_host in hosts:
        return hosts[selected_host]['HostName'], hosts[selected_host]['User']
    else:
        user = input("Enter the username for the IP: ")
        return selected_host, user


def ssh_copy(ip, user, folder_path, remote_path, direction):
    # Überprüfen, ob der Ordner existiert (nur beim Upload relevant)
    if direction == "to" and not os.path.exists(folder_path):
        print(f"Ordnerpfad {folder_path} existiert nicht.")
        return

    if direction == "to":
        print(f"Kopiere {folder_path} nach {ip}:{remote_path}")
        # Erstelle den SCP-Befehl für Upload
        scp_command = ["scp", "-r", folder_path, f"{user}@{ip}:{remote_path}"]
    else:
        print(f"Kopiere {ip}:{remote_path} nach {folder_path}")
        # Erstelle den SCP-Befehl für Download
        scp_command = ["scp", "-r", f"{user}@{ip}:{remote_path}", folder_path]

    try:
        # Führe den SCP-Befehl aus
        subprocess.run(scp_command, check=True)
        if direction == "to":
            print(
                f"Erfolgreich kopiert: {folder_path} nach {ip}:{remote_path}")
        else:
            print(
                f"Erfolgreich kopiert: {ip}: {remote_path} nach {folder_path}")
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Kopieren: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='SSH Kopie von oder zu einem Server.')
    parser.add_argument('folder', type=str,
                        help='Pfad des Ordners (lokal oder remote)')
    parser.add_argument('remote_path', type=str,
                        help='Pfad auf dem Server (lokal oder remote)')
    parser.add_argument('direction', choices=[
                        'to', 'from'], help="Gib 'to' für Upload oder 'from' für Download an")

    args = parser.parse_args()

    # Host/IP auswählen
    ip, user = choose_host_or_ip()

    print(args.remote_path)

    # SSH Kopie durchführen
    ssh_copy(ip, user, args.folder, args.remote_path, args.direction)


if __name__ == "__main__":
    main()
