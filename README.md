---

# 🐞 BugRescue V2.0

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Multi-Cloud](https://img.shields.io/badge/AI-OpenAI%20%7C%20Claude%20%7C%20Gemini-purple)](https://openai.com/)

> **"Your Hybrid AI Code Surgeon."**
> BugRescue fixes bugs in real-time. Use **Local AI** for privacy, or switch to **Cloud AI** (OpenAI, Claude, Gemini) for complex logic.

---

## ⚡ Key Features

| Feature           | Description                                                                          |
| :---------------- | :----------------------------------------------------------------------------------- |
| **Hybrid Brain**  | Switch between `ollama` (default), `openai`, `anthropic`, or `gemini` with one flag. |
| **Auto-Fix Loop** | Runs code → Catches error → Patches code → Repeats until fixed.                      |
| **Polyglot**      | Supports Python, JavaScript, Go, Rust, C++, Java, and more.                          |
| **Safety First**  | Auto-backups (`.bugrescue_backups/`) and Dry-Run mode.                               |

---

## 🚀 Usage

### 1. Default (Local / Privacy Mode)

Uses Ollama (`qwen2.5-coder`) running on your machine.

```bash
python3 bug_rescue.py ./my-project
```

---

### 2. Cloud Mode (OpenAI / Claude / Gemini)

For tougher bugs, use a smarter cloud model.

```bash
# OpenAI
python3 bug_rescue.py ./my-project --provider openai --key "sk-..."

# Anthropic (Excellent for coding)
python3 bug_rescue.py ./my-project --provider anthropic --key "sk-ant-..."

# Google Gemini (Fast & Large Context)
python3 bug_rescue.py ./my-project --provider gemini --key "AIza..."
```

---

### 3. Docker (Enterprise / CI)

```bash
docker run --rm -it \
  -v $(pwd):/code \
  bugrescue/engine /code \
  --provider openai --key "sk-..."
```

---

## 🛠️ Configuration

| Flag         | Description                                                  | Default       |
| ------------ | ------------------------------------------------------------ | ------------- |
| `--provider` | Choose AI: `ollama`, `openai`, `anthropic`, `gemini`         | `ollama`      |
| `--key`      | API key for cloud providers                                  | `None`        |
| `--model`    | Override default model (e.g., `gpt-4o`, `claude-3.5-sonnet`) | Smart default |
| `--dry-run`  | Audit only, no file changes                                  | `False`       |

---

## 🔒 Safety Guarantees

* Automatic backups before every change
* Human-readable patch diffs
* Dry-run mode for auditing fixes
* No cloud calls in local mode

---

## 📄 License

MIT License

---
