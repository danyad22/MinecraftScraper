import random
import socket
import minestat
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style

print(f"{Fore.LIGHTBLUE_EX}\n        _                            __ _   __                                \n  /\/\ (_)_ __   ___  ___ _ __ __ _ / _| |_/ _\ ___ _ __ __ _ _ __   ___ _ __ \n /    \| | '_ \ / _ \/ __| '__/ _` | |_| __\ \ / __| '__/ _` | '_ \ / _ \ '__|\n/ /\/\ \ | | | |  __/ (__| | | (_| |  _| |__\ \ (__| | | (_| | |_) |  __/ |   \n\/    \/_|_| |_|\___|\___|_|  \__,_|_|  \__\__/\___|_|  \__,_| .__/ \___|_|   \n                                                             |_|              \n{Style.RESET_ALL}")

def scan_port():
    for i in range(1, 50000):
        try:
            ip = f"{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
            port = 25565
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.13)
            s.connect((ip, port))
            s.send(b'\xFE\x01')
            get = s.recv(1024)
            if b'\xff' in get:
                get = get[16::]
            conv = get.decode('utf-16', errors='ignore')
            #print(f"{Fore.YELLOW}[+]{ip}:{port} is open and maybe a Minecraft server: {conv}{Style.RESET_ALL}")
            if conv != '':
                #print(f"Scanning {ip}:{port} recv: {conv}")
                ms = minestat.MineStat(ip, port)
                ms.fullstat_query()
                bad_chars = ['§0', '§1', '§2', '§3', '§4', '§5', '§6', '§7', '§8', '§9', '§a', '§b', '§c', '§d', '§e', '§f',
                             '§g', '§k', '§l', '§m', '§n', '§o', '§r', '$']
                for bad in bad_chars:
                    conv = conv.replace(bad, '')
                if ms.online: # and ms.current_players > 0
                    print("------------------------------------")
                    print(f"{Fore.GREEN}[+]{ip}:{port} is open and Minecraft server{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}Latency: %sms" % ms.latency + Style.RESET_ALL)
                    if ms.current_players > 0:
                        print(f'{Fore.LIGHTRED_EX}Players: %s' % ms.current_players + Style.RESET_ALL)
                    else:
                        print(f'{Fore.YELLOW}Players: %s' % ms.current_players + Style.RESET_ALL)
                    print(f'{Fore.YELLOW}Player list: %s' % ms.player_list + Style.RESET_ALL)
                    print(f'{Fore.YELLOW}Max players: %s' % ms.max_players + Style.RESET_ALL)
                    print(f'{Fore.YELLOW}Plugins: %s' % ms.plugins + Style.RESET_ALL)
                    print(f'{Fore.YELLOW}Map: %s' % ms.map + Style.RESET_ALL)
                    print(f'{Fore.YELLOW}Raw version and description: %s' % conv + Style.RESET_ALL)
                    current_datetime = datetime.now()
                    print(f'{Fore.YELLOW}Current date and time of hit: %s' % current_datetime + Style.RESET_ALL)
                    if ms.gamemode:
                        print(f'{Fore.YELLOW}Game mode: %s' % ms.gamemode + Style.RESET_ALL)
                    print(f'{Fore.YELLOW}Connected using protocol: %s' % ms.slp_protocol + Style.RESET_ALL)
                    print("------------------------------------")
        except socket.error:
            pass
        except Exception as e:
            if not isinstance(e, socket.error):
                print(f"{Fore.RED}[!] {ip}:{port} - {e.__class__.__name__}: {e}{Style.RESET_ALL}")
        finally:
            s.close()

def main():
    with ThreadPoolExecutor(max_workers=2500) as executor:
        futures = [executor.submit(scan_port) for _ in range(810)]
        for future in as_completed(futures):
            future.result()

if __name__ == "__main__":
    main()
