# Base Image: Lightweight Python
FROM python:3.10-slim

# 1. Install System Dependencies (Compilers & Runtimes)
# We install Go, Node.js, Java, C++, Rust, and Curl to support polyglot repairs.
RUN apt-get update && apt-get install -y \
    golang-go \
    nodejs \
    npm \
    default-jdk \
    g++ \
    rustc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 2. Setup Working Directory
WORKDIR /app

# 3. Install Python Dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# 4. Copy the BugRescue Engine
COPY bug_rescue.py /usr/local/bin/bug-rescue

# 5. Make it Executable
RUN chmod +x /usr/local/bin/bug-rescue

# 6. Set Entrypoint
# This allows users to run it like a binary: "docker run bugrescue /path/to/code"
ENTRYPOINT ["python3", "/usr/local/bin/bug-rescue"]