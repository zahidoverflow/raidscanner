### **Vulnerability Scanner** is an easy-to-use tool that finds web issues like `LFI` - `OR` - `SQLi` - `XSS` - `CRLF`.

[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-zahidoverflow%2Fraidscanner-blue?logo=docker)](https://hub.docker.com/r/zahidoverflow/raidscanner)
[![Docker Image Size](https://img.shields.io/docker/image-size/zahidoverflow/raidscanner/latest)](https://hub.docker.com/r/zahidoverflow/raidscanner)
[![Docker Pulls](https://img.shields.io/docker/pulls/zahidoverflow/raidscanner)](https://hub.docker.com/r/zahidoverflow/raidscanner)

## 🎨 New: Web-Based GUI

RaidScanner now features a modern web interface! Run the tool through your browser with real-time updates.

**Quick Start:**
```bash
docker-compose up raidscanner-web
# Access at http://localhost:5000
```

👉 **[See Web GUI Documentation](WEB_GUI.md)** for detailed setup and usage.

## Features

| Features                          | About                                                                       |
|-----------------------------------|-----------------------------------------------------------------------------|
| `🌐 Web GUI`                      | Modern web interface with real-time updates (NEW!)                          |
| `LFI Scanner`                     | Detect Local File Inclusion vulnerabilities.                                |
| `OR Scanner`                      | Identify Open Redirect vulnerabilities.                                     |
| `SQL Scanner`                     | Detect SQL Injection vulnerabilities.                                       |
| `XSS Scanner`                     | Identify Cross-Site Scripting vulnerabilities.                              |
| `CRLF Scanner`                    | Detect Carriage Return Line Feed Injection vulnerabilities.                 |
| `Multi-threaded Scanning`         | Improved performance through multi-threading.                               |
| `Customizable Payloads`           | Adjust payloads to suit specific targets.                                   |
| `Success Criteria`                | Modify success detection criteria for specific use cases.                   |
| `User-friendly CLI`               | Simple and intuitive command-line interface.                                |
| `Save Vulnerable URLs`            | Option to save vulnerable URLs to a file for future reference.              |
| `HTML Report Generation`          | Generates a detailed HTML report of found vulnerabilities.                  |
<!-- | `Share HTML Report via Telegram`  | Share HTML vulnerability reports directly through Telegram.                 | -->

<br>
<hr>
<br>
<br>

| Language                          | Packages                                                                    |
|-----------------------------------|-----------------------------------------------------------------------------|
| ***Python***| `Python 3.x` `webdriver_manager` `selenium` `aiohttp` `beautifulsoup4` `colorama` `rich` `requests` `gitpython` `prompt_toolkit` `pyyaml` `Flask` `flask-socketio`|

<br>
<hr>
<br>

## Installation

### Option 1: Docker (Recommended - Easy & Portable)

**Pull from Docker Hub (fastest):**
```bash
# CLI Mode
docker pull zahidoverflow/raidscanner:latest
docker run -it --rm \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/reports:/app/reports \
  --shm-size=2g \
  zahidoverflow/raidscanner:latest

# Web GUI Mode
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/reports:/app/reports \
  -e MODE=web \
  --shm-size=2g \
  zahidoverflow/raidscanner:latest
```

**Or build locally:**
```bash
# Build and run with docker-compose
docker-compose build
docker-compose run --rm raidscanner

# Or use the convenience script
chmod +x docker-run.sh
./docker-run.sh
```

📖 **See [DOCKER.md](DOCKER.md) for complete Docker documentation**

**Benefits:**
- ✅ No manual dependency installation
- ✅ Isolated environment
- ✅ Works on Windows, Mac, Linux
- ✅ Pre-configured Chrome & ChromeDriver
- ✅ Easy to share and deploy
- ✅ Available on Docker Hub

---

### Option 2: Manual Installation

**Clone the repository:**
```bash
git clone https://github.com/zahidoverflow/raidscanner.git
cd raidscanner
```

**Install the requirements:**
```bash
pip3 install -r requirements.txt
```

**Run the Script:**
```bash
python3 main.py
```

----

| Input Information         |                                                                                         |
|---------------------------|-----------------------------------------------------------------------------------------|
| Input URL/File            | Provide a single URL or an input file containing multiple URLs for scanning.            |
| Payload File              | Select or provide a custom payload file for the specific type of vulnerability scanning.|
| Success Criteria          | Define patterns or strings indicating a successful exploitation attempt.                |
| Concurrent Threads        | Set the number of threads for multi-threaded scanning.                                  |
| View and Save Results     | Display results in real-time during the scan, and save vulnerable URLs for future use.  |

----

| Customization              |                                                                                          |
|----------------------------|------------------------------------------------------------------------------------------|
| Custom Payloads            | Modify or create payload files for different vulnerability types to target specific apps.|
| Success Criteria           | Adjust the tool's success patterns to more accurately detect successful exploitations.   |
| Concurrent Threads         | Control the number of threads used during the scan for performance optimization.         |


----

### Chrome Installation

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
```

```bash
sudo dpkg -i google-chrome-stable_current_amd64.deb
```

- If you encounter any errors during installation, use the following command:

```bash
sudo apt -f install
```

```bash
sudo dpkg -i google-chrome-stable_current_amd64.deb
```

----

### Chrome Driver Installation

```bash
wget https://storage.googleapis.com/chrome-for-testing-public/128.0.6613.119/linux64/chromedriver-linux64.zip
```
```bash
unzip chromedriver-linux64.zip
```
```bash
cd chromedriver-linux64 
```
```bash
sudo mv chromedriver /usr/bin
```
<hr>

> [!WARNING]  
> This scanner is intended for educational and ethical hacking purposes only. It should only be used to test systems you own or have explicit permission to test. Unauthorized use of third-party websites or systems without consent is illegal and unethical.



