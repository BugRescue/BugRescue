#!/usr/bin/env python3
"""
🐞 BUGRESCUE V2.0: HYBRID EDITION
Autonomous Code Repair with Multi-Cloud Support (Ollama, OpenAI, Anthropic, Gemini).
"""
import subprocess, sys, os, re, requests, argparse, shutil, html, time, json
from datetime import datetime

# --- AUTO-INSTALL DEPENDENCIES ---
def install_deps():
    try:
        import tqdm, colorama
    except ImportError:
        pass
try:
    from tqdm import tqdm
    from colorama import Fore, Back, Style, init
except ImportError:
    print("⚠️  Dependencies missing. Run: pip install -r requirements.txt")
    sys.exit(1)

# CONFIG & CONSTANTS
VERSION = "v2.0.0-Hybrid"
BACKUP_DIR = ".bugrescue_backups"
REPORT_FILE = "bugrescue_report.html"

# Initialize Colors
init(autoreset=True)

# --- AI PROVIDER LOGIC ---
class AIProvider:
    def __init__(self, args):
        self.provider = args.provider
        self.key = args.key or os.getenv(f"{args.provider.upper()}_API_KEY")
        self.model = args.model
        self.url = args.url

        # Set Defaults if not provided
        if self.provider == "ollama":
            self.url = self.url or "http://localhost:11434/api/generate"
            self.model = self.model or "qwen2.5-coder:14b"
        elif self.provider == "openai":
            self.url = "https://api.openai.com/v1/chat/completions"
            self.model = self.model or "gpt-4o"
        elif self.provider == "anthropic":
            self.url = "https://api.anthropic.com/v1/messages"
            self.model = self.model or "claude-3-5-sonnet-20240620"
        elif self.provider == "gemini":
            self.model = self.model or "gemini-1.5-pro"
            self.url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.key}"

    def query(self, prompt):
        try:
            if self.provider == "ollama":
                res = requests.post(self.url, json={"model": self.model, "prompt": prompt, "stream": False, "options": {"temperature": 0.2}}, timeout=120)
                return res.json().get('response', '')

            elif self.provider == "openai":
                if not self.key: return "ERROR: Missing OpenAI API Key."
                headers = {"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"}
                payload = {
                    "model": self.model,
                    "messages": [{"role": "system", "content": "You are a Senior Engineer."}, {"role": "user", "content": prompt}],
                    "temperature": 0.2
                }
                res = requests.post(self.url, headers=headers, json=payload, timeout=60)
                return res.json()['choices'][0]['message']['content']

            elif self.provider == "anthropic":
                if not self.key: return "ERROR: Missing Anthropic API Key."
                headers = {"x-api-key": self.key, "anthropic-version": "2023-06-01", "content-type": "application/json"}
                payload = {
                    "model": self.model,
                    "max_tokens": 4096,
                    "messages": [{"role": "user", "content": prompt}]
                }
                res = requests.post(self.url, headers=headers, json=payload, timeout=60)
                return res.json()['content'][0]['text']

            elif self.provider == "gemini":
                if not self.key: return "ERROR: Missing Gemini API Key."
                payload = {"contents": [{"parts": [{"text": prompt}]}]}
                res = requests.post(self.url, json=payload, timeout=60)
                return res.json()['candidates'][0]['content']['parts'][0]['text']

        except Exception as e:
            return f"API ERROR: {str(e)}"
        return ""

# --- CORE UTILS ---
def print_banner(provider, model):
    banner = f"""
    {Fore.CYAN}
      ____              ____                           
     |  _ \            |  _ \                          
     | |_) |_   _  __ _| |_) |___  ___  ___ _   _  ___ 
     |  _ <| | | |/ _` |  _ <| _ \/ __|/ __| | | |/ _ \\
     | |_) | |_| | (_| | |_) |  __/\__ \ (__| |_| |  __/
     |____/ \__,_|\__, |____/ \___||___/\___|\__,_|\___|
                   __/ |                                
    {Fore.WHITE}  Autonomous Repair Agent | {VERSION}
    {Fore.YELLOW}  ⚡ Engine: {provider.upper()} ({model})
    {Style.RESET_ALL}"""
    print(banner)

def generate_report(stats, logs):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    css = "body{font-family:'Segoe UI',sans-serif;background:#1e1e1e;color:#d4d4d4;padding:20px;max-width:1000px;margin:0 auto} h1{color:#4ec9b0;border-bottom:1px solid #3c3c3c} .card{background:#252526;border:1px solid #3c3c3c;padding:15px;margin-bottom:20px;border-radius:6px} table{width:100%;border-collapse:collapse} th,td{padding:10px;border-bottom:1px solid #3c3c3c;text-align:left} .success{color:#6a9955} .fail{color:#f44747} .warn{color:#cca700}"
    rows = "".join([f"<tr><td>{e['file']}</td><td class='{'success' if e['status']=='FIXED' else 'fail'}'><strong>{e['status']}</strong></td><td>{html.escape(e['error'])[:120]}</td></tr>" for e in logs])
    html_c = f"<html><head><title>BugRescue Report</title><style>{css}</style></head><body><h1>🐞 BugRescue Audit Report</h1><div class='card' style='display:flex;gap:20px;text-align:center'><div style='flex:1'><h2 class='success'>{stats['passed']}</h2>Fixed</div><div style='flex:1'><h2 class='fail'>{stats['failed']}</h2>Failed</div></div><div class='card'><h3>Audit Log ({timestamp})</h3><table><tr><th>File</th><th>Status</th><th>Detection</th></tr>{rows}</table></div></body></html>"
    with open(REPORT_FILE, "w") as f: f.write(html_c)
    return os.path.abspath(REPORT_FILE)

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
    return f"Act as a Principal Engineer. Fix this code.\nERROR: {error[-1500:]}\nCODE: {code}\nINSTRUCTION: Return ONLY the fixed code block. No explanations."

def clean(raw):
    m = re.search(r"```(?:\w+)?\s*\n(.*?)```", raw, re.DOTALL)
    return m.group(1).strip() if m else raw.replace("```", "").strip()

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("path", help="Project path to scan")
    parser.add_argument("--dry-run", action="store_true", help="Audit only (no changes)")
    parser.add_argument("--provider", default="ollama", choices=["ollama", "openai", "anthropic", "gemini"], help="AI Provider to use")
    parser.add_argument("--key", help="API Key for cloud providers")
    parser.add_argument("--model", help="Override default model (e.g. gpt-4-turbo)")
    parser.add_argument("--url", help="Override Ollama URL")
    args = parser.parse_args()

    ai = AIProvider(args)
    print_banner(ai.provider, ai.model)
    
    files = []
    for r, _, fs in os.walk(args.path):
        if ".bugrescue_backups" in r: continue
        for f in fs:
            if f.endswith(('.py','.js','.go','.rs','.cpp','.java','.php','.rb','.sh','.yaml','.html','Dockerfile')):
                files.append(os.path.join(r, f))
    
    if not files:
        print(f"{Fore.RED}❌ No scannable files found.{Style.RESET_ALL}")
        return

    print(f"{Fore.YELLOW}🚀 Launching on {len(files)} Artifacts...{Style.RESET_ALL}")
    
    if not args.dry_run:
        os.makedirs(BACKUP_DIR, exist_ok=True)
    
    stats = {'passed': 0, 'failed': 0}
    logs = []
    
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
                if i == 1: # Backup original on first failure
                    shutil.copy2(f, os.path.join(BACKUP_DIR, f"{fname}.bak"))
                
                with open(f, 'r') as fl: c = fl.read()
                fix = clean(ai.query(get_prompt(c, entry['error'])))
                if len(fix) > 10:
                    with open(f, 'w') as fl: fl.write(fix)
        
        if not fixed:
            entry['status'] = "FAILED"
            stats['failed'] += 1
            tqdm.write(f"{Fore.RED}✘ Failed: {fname}{Style.RESET_ALL}")
        
        logs.append(entry)

    report = generate_report(stats, logs)
    print(f"\n{Fore.GREEN}✔ Rescue Complete!{Style.RESET_ALL}")
    print(f"📊 Report: {Fore.BLUE}{report}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
