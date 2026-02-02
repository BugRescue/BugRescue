# 🐞 BugRescue

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Docker Ready](https://img.shields.io/badge/docker-ready-green.svg)](https://hub.docker.com/)

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

### 🐳 Docker (Recommended)
Zero setup. Runs in an isolated container.
```bash
docker run --rm -it \
  -v $(pwd):/code \
  -e OLLAMA_URL="http://host.docker.internal:11434/api/generate" \
  bugrescue/engine /code
