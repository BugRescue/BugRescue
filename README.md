# 🐞 BugRescue

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Docker Ready](https://img.shields.io/badge/docker-ready-green.svg)](https://hub.docker.com/)
[![Powered By](https://img.shields.io/badge/AI-Qwen2.5-purple.svg)](https://ollama.com/)

> **"Your Autonomous Code Surgeon."**
> BugRescue finds crashes, compiles code, and fixes bugs in real-time using local AI.

---

## ⚡ Why BugRescue?
Most tools just *tell* you what's wrong. **BugRescue fixes it.**
It runs your code, watches it crash, analyzes the stack trace, and rewrites the source code until it passes.

| Language | Support Level |
| :--- | :--- |
| **Python** | 🔥 Full Support (Runtime & Logic) |
| **JavaScript** | ⚡ Node.js Runtime Support |
| **Go / Rust** | 🦀 Compilation & Concurrency |
| **C++ / Java** | ☕ Memory Safety & Null Checks |

---

## 🚀 Instant Start

### 🐳 Option A: Docker (Recommended)
Zero setup. Runs in an isolated container with all compilers (Rust, Go, Java) pre-installed.

```bash
docker run --rm -it \
  -v $(pwd):/code \
  -e OLLAMA_URL="[http://host.docker.internal:11434/api/generate](http://host.docker.internal:11434/api/generate)" \
  bugrescue/engine /code

```

### 🐍 Option B: Manual Install

Use this if you want to run it directly on your machine.
*Prerequisites: Python 3.10+, Ollama running locally.*

```bash
# 1. Clone the repo
git clone [https://github.com/BugRescue/bug-rescue.git](https://github.com/BugRescue/bug-rescue.git)
cd bug-rescue

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the Rescue Agent
python3 bug_rescue.py /path/to/your/broken/project

```

---

## 📊 Key Features

* **🛡️ Auto-Backup:** Never lose code. Before touching any file, a snapshot is saved to `.bugrescue_backups/`.
* **📈 HTML Dashboard:** Generates a visual report (`bugrescue_report.html`) after every run showing pass/fail stats.
* **🧪 Dry-Run Mode:** Use the `--dry-run` flag to see exactly what the AI *would* fix without actually modifying your files.
* **🧠 Local & Private:** Powered by Ollama. Your code never leaves your machine.

---

## 🛠️ Usage & Flags

```bash
usage: bug_rescue.py [-h] [--dry-run] path

positional arguments:
  path        Project path to scan (e.g., ./my-project)

options:
  -h, --help  show this help message and exit
  --dry-run   Audit only. Generates report but does not edit files.

```

---

## 🧠 Supported Vulnerabilities

BugRescue is trained to detect and fix:

* **Security:** SQL Injection, Hardcoded Secrets, Insecure Randomness.
* **Concurrency:** Race Conditions (Go/Rust), Deadlocks.
* **Logic:** Null Pointers, Type Errors, Syntax Crashes.
* **Infrastructure:** Dangerous Dockerfile configurations.

---

## 🤝 Contributing

Open a PR to add support for more languages!

**License:** MIT
