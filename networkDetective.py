import socket
import sys
import concurrent.futures
import argparse
import subprocess
from tqdm import tqdm
from tabulate import tabulate
from colorama import init, Fore, Style

# Global variables to store results
ip_results = []
port_results = []

def print_banner():
    banner = r"""
            ⢀⡀⠀⢀⡀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣤⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⢸⣿⡄⢸⣇⡾⠟⠓⠛⣿⠓⢿⡇⢀⣤⡀⢸⡇⣰⠟⢳⡄⣿⠙⣷⡇⢀⡇⠀⠀⣿⠉⠻⣷⣴⠿⠛⠚⢻⠛⠂⡾⠟⠃⡴⠲⠖⠛⣿⠓⢲⣾⣧⠀⢸⡗⡾⠟⠃
        ⢸⠉⢷⣸⣿⡷⠶⠆⠀⣿⠀⠘⣇⣼⠻⡇⣿⠁⣯⠀⠀⣻⣿⣾⠃⣿⣿⠁⠀⠀⣿⠀⢠⡿⣿⠶⠖⠀⢸⠀⢸⡷⠶⢸⡇⠀⠀⠀⣿⠀⢸⡏⢿⡀⡿⢹⡷⠶⠆
        ⢸⠀⠈⢿⡟⣷⣤⠶⠀⡿⠀⠀⢻⡿⠀⢻⡟⠀⠻⢦⡴⠟⢿⠘⣧⣧⠙⣧⠀⠀⣿⣴⡿⠁⢿⣤⡶⠀⢸⠀⠸⣧⣤⠎⠷⣴⡆⠀⣿⠀⢸⡇⠘⣿⠇⠸⣧⣴⠆
    """

    print(Fore.RED + Style.BRIGHT + banner + Fore.GREEN)

def check_ip(ip, progress_bar, verbose):
    try:
        # Ping command depending on the operating system
        ping_command = ["ping", "-c", "1", ip]  # For Unix-based operating systems

        # Execute the ping command
        process = subprocess.Popen(ping_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, error = process.communicate()

        if process.returncode == 0:
            ip_results.append({"IP": ip, "Status": "Active"})

        if error and verbose:
            print(f"Error for {ip}: {error.decode('utf-8')}")

    except Exception as e:
        print(f"Error for {ip}: {e}")
    finally:
        progress_bar.update(1)

def check_port(ip, port, progress_bar, verbose):
    try:
        socketObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketObj.settimeout(1)  # 1-second timeout for the connection

        res = socketObj.connect_ex((ip, port))
        if res == 0:
            port_results.append({"IP": ip, "Port": port, "Status": "Open"})
            if verbose:
                print(f"Port {port} Open on {ip}")

    except Exception as e:
        if verbose:
            print(f"Error on port {port} on {ip}: {e}")
    finally:
        socketObj.close()
        progress_bar.update(1)

def check_banner(ip, port):
    try:
        socketObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketObj.settimeout(1)  # 1-second timeout for the connection

        socketObj.connect((ip, port))
        banner = socketObj.recv(1024).decode('utf-8').strip()
        print(f"Banner on port {port} on {ip}: {banner}")
    except Exception as e:
        print(f"Error getting banner on port {port} on {ip}: {e}")
    finally:
        socketObj.close()

def scan_network(network, verbose):
    try:
        ip_list = [f"{network}.{i}" for i in range(1, 255)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            progress_bar = tqdm(total=len(ip_list), desc="IP Scan", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}", colour='red', ncols=80)
            list(executor.map(lambda ip: check_ip(ip, progress_bar, verbose), ip_list))
    except KeyboardInterrupt:
        print("\nScan interrupted by the user.")

def port_scan(ip, max_port, verbose):
    try:
        total_ports = min(max_port, 65535)
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            port_list = range(1, total_ports + 1)
            progress_bar = tqdm(total=total_ports, desc="Port Scan", bar_format="{l_bar}{bar}| Port {n_fmt}/{total_fmt}", colour='red', ncols=80)
            list(executor.map(lambda port: check_port(ip, port, progress_bar, verbose), port_list))
    except KeyboardInterrupt:
        print("\nPort Scan interrupted by the user.")

def display_results():
    if ip_results != []:
        print("\nIP Scan Results:")
        print(tabulate(ip_results, headers="keys"))
    if port_results != []:
        print("\nPort Scan Results:")
        print(tabulate(port_results, headers="keys"))

def arg_options():
    options_table = [
        ["-s, --scan <NETWORK>", "Check active IPs on a network"],
        ["-ps, --portscan <IP>", "Check open ports on an IP"],
        ["-mp, --maxport <PORT>", "Specify the maximum port for Port Scan"],
        ["-b, --banner <IP> <PORT>", "Check the banner on a specific port"],
        ["-v, --verbose", "Display detailed messages"]
    ]

    usage_text = f"Usage: python main.py [OPTION] [ARGUMENT]\n\nOptions and Arguments:\n{tabulate(options_table, tablefmt='grid')}\n\nExamples:\n\n- Check active IPs on a network:\n  python main.py -s 192.168.1.0\n\n- Check open ports on an IP:\n  python main.py -ps 192.168.1.1\n\n- Check the banner on a specific port:\n  python main.py -b 192.168.1.1 80"

    print(usage_text)

def main():
    # Print BANNER
    print_banner()

    parser = argparse.ArgumentParser(description="Script for IP and Port Scan.")
    parser.add_argument("-s", "--scan", metavar="NETWORK", help="Check active IPs on a network")
    parser.add_argument("-ps", "--portscan", metavar="IP", help="Check open ports on an IP")
    parser.add_argument("-b", "--banner", metavar=("IP", "PORT"), nargs=2, help="Check the banner on a specific port")
    parser.add_argument("-v", "--verbose", action="store_true", help="Display detailed messages")
    parser.add_argument("-mp", "--maxport", type=int, default=65535, help="Specify the maximum port for Port Scan")

    args = parser.parse_args()

    if args.scan:
        scan_network(args.scan, args.verbose)
    elif args.portscan:
        port_scan(args.portscan, args.maxport, args.verbose)
    elif args.banner:
        ip, port = args.banner
        check_banner(ip, int(port))
    else:
        arg_options()

    # Display results at the end of the script
    if args.scan or args.portscan:
        display_results()

if __name__ == '__main__':
    main()
