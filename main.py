import threading
import random
import socket
import minestat
from colorama import Fore, Style

def scan_port():
    for i in range(1, 10000):
        try:
            ip = f"{random.randint(36,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            port = 25565
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(random.randint(100,200)/1000)
            s.connect((ip, port))
            s.send(b'\xFE\x01')
            get = s.recv(1024)
            if b'\xff' in get:
                get = get[16::]
            conv = get.decode('utf-16', errors='ignore')
            #print(f"{Fore.LIGHTBLUE_EX}[+]{ip}:{port} is open, checking for minecraft server, response: {conv}{Style.RESET_ALL}")
            ms = minestat.MineStat(ip, port)
            ms.beta_query()
            bad_chars = ['§0', '§1', '§2', '§3', '§4', '§5', '§6', '§7', '§8', '§9', '§a', '§b', '§c', '§d', '§e', '§f',
             '§g', '§k', '§l', '§m', '§n', '§o', '§r']
            for bad in bad_chars:
                if bad in conv:
                    conv = conv.replace(bad, '')
            if ms.online: #and ms.current_players > 0
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
                if ms.gamemode:
                    print(f'{Fore.YELLOW}Game mode: %s' % ms.gamemode + Style.RESET_ALL)
                print(f'{Fore.YELLOW}Connected using protocol: %s' % ms.slp_protocol + Style.RESET_ALL)
                print("------------------------------------")
        except socket.error as e:
            pass
            #print(f"{Fore.RED}[!] {ip}:{port} - {e}{Style.RESET_ALL}")
        except Exception as e:
            if not isinstance(e, socket.error):
                print(f"{Fore.RED}[!] {ip}:{port} - {e.__class__.__name__}: {e}{Style.RESET_ALL}")
        finally:
            s.close()

def main():
    threads = []
    for i in range(610): #Change it based on your system
        t = threading.Thread(target=scan_port)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
main()
