import os
import pyperclip
import platform
import socket
import re
import uuid
import requests
import whois

def capture_clipboard():
    try:
        return pyperclip.paste()
    except Exception as e:
        print(f"Error capturing clipboard content: {e}")
        return None

def get_system_info():
    try:
        info = {
            'platform': platform.system(),
            'platform-release': platform.release(),
            'platform-version': platform.version(),
            'architecture': platform.machine(),
            'hostname': socket.gethostname(),
            'ip-address': socket.gethostbyname(socket.gethostname()),
            'mac-address': ':'.join(re.findall('..', '%012x' % uuid.getnode())),
            'processor': platform.processor(),
        }

        try:
            response = requests.get('https://api.ipify.org?format=json')
            info['global-ip-address'] = response.json().get('ip', 'N/A')
        except Exception:
            info['global-ip-address'] = 'Could not fetch global IP address'

        return info
    except Exception as e:
        print("Error capturing system info:", e)
        return {}

def get_headers(domain):
    try:
        response = requests.get("http://" + domain)
        print("\n[+] HTTP Headers:")
        for key, value in response.headers.items():
            print(f"   {key}: {value}")
    except:
        print("[-] Could not fetch headers.")

def get_whois(domain):
    try:
        info = whois.whois(domain)
        print("\n[+] WHOIS Info:")
        print(f"   Domain Name: {info.domain_name}")
        print(f"   Registrar: {info.registrar}")
        print(f"   Creation Date: {info.creation_date}")
    except:
        print("[-] WHOIS lookup failed.")

def get_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        print(f"[+] IP Address: {ip}")
    except:
        print("[-] Could not resolve domain.")

if __name__ == '__main__':
    clipboard_content = capture_clipboard()
    if clipboard_content:
        print('\nClipboard Content:')
        print(clipboard_content)

    system_info = get_system_info()
    print('\nSystem Information:')
    for key, value in system_info.items():
        print(f'{key}: {value}')
        
    domain = input("Enter domain (e.g. example.com): ")
    get_ip(domain)
    get_headers(domain)
    get_whois(domain)
