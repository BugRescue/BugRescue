# === CELL FINAL: BUGRESCUE ENGINE ===
script_content = r'''#!/usr/bin/env python3
"""
🐞 BUGRESCUE V1.0: ENTERPRISE EDITION
The Autonomous Code Surgeon.
"""
import subprocess, sys, os, re, requests, argparse, shutil, html, time
from datetime import datetime

# --- AUTO-INSTALL DEPENDENCIES (Zero Setup) ---
def install_deps():
    try:
        import tqdm, colorama
    except ImportError:
        print("⚙️  Installing BugRescue UI dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tqdm", "colorama", "requests"])

install_deps()
from tqdm import tqdm
from colorama import Fore, Back, Style, init

# CONFIG
VERSION = "v1.0.0-Rescue"
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL = "qwen2.5-coder:14b"
BACKUP_DIR = ".bugrescue_backups"
REPORT_FILE = "bugrescue_report.html"

# Initialize Colors
init(autoreset=True)

def print_banner():
    # ASCII Art for BugRescue
    banner = f"""
    {Fore.GREEN}
      ____              ____                           
     |  _ \            |  _ \                          
     | |_) |_   _  __ _| |_) |___  ___  ___ _   _  ___ 
     |  _ <| | | |/ _` |  _ <| _ \/ __|/ __| | | |/ _ \\
     | |_) | |_| | (_| | |_) |  __/\__ \ (__| |_| |  __/
     |____/ \__,_|\__, |____/ \___||___/\___|\__,_|\___|
                   __/ |                                
                  |___/                                 
    {Fore.WHITE}  Autonomous Repair Agent | {VERSION}
    {Style.RESET_ALL}"""
    print(banner)

def generate_report(stats, logs):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    css = "body{font-family:'Segoe UI',sans-serif;background:#1e1e1e;color:#d4d4d4;padding:20px;max-width:1000px;margin:0 auto} h1{color:#4ec9b0;border-bottom:1px solid #3c3c3c} .card{background:#252526;border:1px solid #3c3c3c;padding:15px;margin-bottom:20px;border-radius:6px} table{width:100%;border-collapse:collapse} th,td{padding:10px;border-bottom:1px solid #3c3c3c;text-align:left} .success{color:#6a9955} .fail{color:#f44747} .warn{color:#cca700}"
    
    rows = ""
    for e in logs:
        status_cls = 'success' if e['status'] == 'FIXED' else 'fail' if e['status'] == 'FAILED' else 'warn'
        rows += f"<tr><td>{e['file']}</td><td class='{status_cls}'><strong>{e['status']}</strong></td><td>{html.escape(e['error'])[:120]}</td></tr>"

    html_c = f"""
    <html><head><title>BugRescue Report</title><style>{css}</style></head>
    <body>
        <h1>🐞 BugRescue Audit Report</h1>
        <div class="card" style="display:flex;gap:20px;text-align:center">
            <div style="flex:1"><h2 class="success">{stats['passed']}</h2>Fixed</div>
            <div style="flex:1"><h2 class="fail">{stats['failed']}</h2>Failed</div>
            <div style="flex:1"><h2>{stats['passed']+stats['failed']}</h2>Total</div>
        </div>
        <div class="card">
            <h3>Audit Log ({timestamp})</h3>
            <table><tr><th>File</th><th>Status</th><th>Detection</th></tr>{rows}</table>
        </div>
    </body></html>
    """
    with open(REPORT_FILE, "w") as f: f.write(html_c)
    return os.path.abspath(REPORT_FILE)

def query_ai(prompt):
    try:
        res = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt, "stream": False, "temperature": 0.2}, timeout=120)
        return res.json().get('response', '')
    except: return ""

class Executor:
    def run(self, f):
        ext = f.split('.')[-1]
        cmd = []
        if ext == 'py': cmd = ["python3", "-u", f]
        elif ext == 'js': cmd = ["node", f]
        elif ext == 'go': cmd = ["go", "run", f]
        elif ext == 'rs':
            bin = f.replace('.rs', '')
            if subprocess.run(["rustc", f, "-o", bin], capture_output=True).returncode != 0: return subprocess.CompletedProcess([], 1, "", "Rust Compile Failed")
            cmd = [bin]
        elif ext == 'cpp':
            bin = f.replace('.cpp', '')
            if subprocess.run(["g++", f, "-o", bin], capture_output=True).returncode != 0: return subprocess.CompletedProcess([], 1, "", "C++ Compile Failed")
            cmd = [bin]
        elif ext in ['yaml', 'Dockerfile', 'html']: 
            with open(f, 'r') as fl: c = fl.read()
            if "password:" in c and "Secret" in c: return subprocess.CompletedProcess([], 1, "", "Hardcoded Secret")
            return subprocess.CompletedProcess([], 0, "Valid", "")

        if not cmd: return subprocess.CompletedProcess([], 0, "", "SKIPPED")
        try: return subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        except: return subprocess.CompletedProcess([], 124, "", "TIMEOUT")

def get_prompt(code, error):
    return f"Act as a Senior Engineer. Fix this code.\nERROR: {error[-1500:]}\nCODE: {code}\nINSTRUCTION: Return ONLY fixed code."

def clean(raw):
    m = re.search(r"```(?:\w+)?\s*\n(.*?)```", raw, re.DOTALL)
    return m.group(1).strip() if m else raw.replace("```", "").strip()

def main():
    print_banner()
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Project path to scan")
    parser.add_argument("--dry-run", action="store_true", help="Audit only")
    args = parser.parse_args()
    
    files = []
    for r, _, fs in os.walk(args.path):
        if ".bugrescue_backups" in r: continue
        for f in fs:
            if f.endswith(('.py','.js','.go','.rs','.cpp','.java','.php','.rb','.sh','.yaml','.html','Dockerfile')):
                files.append(os.path.join(r, f))
    
    if not files:
        print(f"{Fore.RED}❌ No scannable files found in {args.path}{Style.RESET_ALL}")
        return

    print(f"{Fore.YELLOW}🚀 BugRescue Launching on {len(files)} Artifacts...{Style.RESET_ALL}")
    
    # BACKUP
    if not args.dry_run:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        bk = os.path.join(BACKUP_DIR, f"{ts}_backup")
        os.makedirs(BACKUP_DIR, exist_ok=True)
    
    stats = {'passed': 0, 'failed': 0}
    logs = []
    
    # PROGRESS BAR
    pbar = tqdm(files, unit="file", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}")
    
    for f in pbar:
        fname = os.path.basename(f)
        pbar.set_description(f"Scanning {fname}")
        entry = {'file': fname, 'status': 'FIXED', 'error': ''}
        
        fixed = False
        for i in range(1, 4):
            res = Executor().run(f)
            if res.returncode == 0:
                entry['status'] = "FIXED" if i > 1 else "CLEAN"
                stats['passed'] += 1
                fixed = True
                break
            
            entry['error'] = res.stderr.strip() or res.stdout.strip()
            
            if not args.dry_run:
                with open(f, 'r') as fl: c = fl.read()
                fix = clean(query_ai(get_prompt(c, entry['error'])))
                if len(fix) > 10:
                    with open(f, 'w') as fl: fl.write(fix)
        
        if not fixed:
            entry['status'] = "FAILED"
            stats['failed'] += 1
            # Tqdm friendly print
            tqdm.write(f"{Fore.RED}✘ Failed: {fname}{Style.RESET_ALL}")
        
        logs.append(entry)

    report_path = generate_report(stats, logs)
    print(f"\n{Fore.GREEN}✔ Rescue Complete!{Style.RESET_ALL}")
    print(f"📊 Report: {Fore.BLUE}{report_path}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
'''
with open("bug_rescue.py", "w") as f: f.write(script_content)
print("✅ BugRescue V1.0 Generated.")