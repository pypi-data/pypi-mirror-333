import json
import re
import subprocess


def add_wifi_connection(ssid: str, password: str, connection_name: str, priority=1) -> None:
    
    try:
        subprocess.run(['sudo', 'nmcli', 'connection', 'add', 'type', 'wifi', 'ifname', 'wlan0', 'con-name', connection_name, 'ssid', ssid, 'connection.autoconnect-priority', str(priority)], check=True)
        subprocess.run(['sudo', 'nmcli', 'connection', 'modify', connection_name, 'wifi-sec.key-mgmt', 'wpa-psk'], check=True)
        subprocess.run(['sudo', 'nmcli', 'connection', 'modify', connection_name, 'wifi-sec.psk', password], check=True)

        # Activate the connection
        try:
            subprocess.run(['sudo', 'nmcli', 'connection', 'up', connection_name], check=True)
            print(f"Added and activated new connection: {connection_name}")
        except:
            print(f"New connection added, but unable to connect: {connection_name}")
        
    except subprocess.CalledProcessError as ex:
        print(f"Failed to add connection: {connection_name}. Error: {ex}")


def remove_wifi_connection(ssid: str) -> None:
    
    try:
        subprocess.run(['sudo', 'nmcli', 'connection', 'delete', ssid], check=True)
        print(f"Removed existing connection: {ssid}")
    except subprocess.CalledProcessError as ex:
        print(f"Failed to remove connection: {ssid}. It might not exist.")


def set_wifi_priority(ssid: str, priority: int) -> None:

    # Example usage:
    # set_wifi_priority("YourSSID", 100)

    try:
        # Get the UUID of the connection
        result = subprocess.run(
            ['nmcli', '-g', 'connection.uuid', 'connection', 'show', ssid],
            capture_output=True, text=True, check=True
        )
        uuid = result.stdout.strip()

        if not uuid:
            raise ValueError(f"Connection {ssid} not found.")

        # Set the autoconnect priority
        subprocess.run(
            ['nmcli', 'connection', 'modify', uuid, 'connection.autoconnect-priority', str(priority)],
            check=True
        )

        # Restart Network Manager to apply the changes
        subprocess.run(['sudo', 'systemctl', 'restart', 'NetworkManager'], check=True)

        print(f"Priority for {ssid} set to {priority}.")

    except subprocess.CalledProcessError as ex:
        print(f"An error occurred while running nmcli: {ex}")

    except ValueError as ex:
        print(ex)


def back_up_connections(backup_file_path: str) -> None:
    # Backup all connection data to a JSON file
    try:
        result = subprocess.run(['sudo', 'nmcli', '--json', 'connection', 'export'], capture_output=True, text=True, check=True)
        connections_data = json.loads(result.stdout)
        
        with open(backup_file_path, 'w') as f:
            json.dump(connections_data, f, indent=4)
        
        print(f"Connections backed up to {backup_file_path}.")

    except subprocess.CalledProcessError as ex:
        print(f"Failed to backup connections. Error: {ex}")


def restore_connections(backup_file_path: str) -> None:
    # Restore all connections from a JSON backup file
    try:
        with open(backup_file_path, 'r') as f:
            connections_data = json.load(f)

        subprocess.run(['sudo', 'nmcli', 'connection', 'delete', 'id', 'all'], check=True)

        for connection in connections_data:
            subprocess.run(['sudo', 'nmcli', 'connection', 'import', 'json', json.dumps(connection)], check=True)
        
        print(f"Connections restored from {backup_file_path}.")

    except (subprocess.CalledProcessError, json.JSONDecodeError) as ex:
        print(f"Failed to restore connections. Error: {ex}")
        

def get_saved_wifi_networks():
    try:
        result = subprocess.run(
            ["nmcli", "-t", "-f", "SSID", "connection", "show"], 
            capture_output=True, text=True, check=True
        )
        ssids = [ssid for ssid in result.stdout.splitlines() if ssid]

        network_info = {
            'saved_networks': ssids,
            'network_count': len(ssids)
        }

        return json.dumps(network_info)
    except subprocess.CalledProcessError as e:
        return json.dumps({
            'error': f"Error getting wireless network list: {e}",
            'saved_networks': [],
            'network_count': 0
        })