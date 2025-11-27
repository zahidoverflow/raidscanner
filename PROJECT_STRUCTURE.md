# RaidScanner Project Structure

## Directory Layout

```
raidscanner/
├── .docker/                    # Docker configuration
│   ├── Dockerfile              # Container build definition
│   ├── docker compose.yml      # Multi-service orchestration
│   └── .dockerignore           # Docker build exclusions
│
├── .git/                       # Git version control
│
├── bin/                        # Binary files and executables
│   ├── chromedriver-linux64/   # ChromeDriver for Linux
│   └── chromedriver-linux64.zip
│
├── core/                       # Core scanning logic
│   ├── __init__.py
│   ├── scanner_engine.py       # Platform-agnostic scanners
│   ├── report_generator.py     # Report creation (HTML/JSON)
│   └── payload_loader.py       # Payload management
│
├── docs/                       # Documentation
│   ├── README.md               # Main documentation
│   ├── WEB_GUI.md              # Web interface guide
│   ├── DOCKER.md               # Docker guide
│   ├── QUICKSTART.md           # Quick start guide
│   ├── ARCHITECTURE.md         # System architecture
│   ├── WORKFLOW.md             # Development workflow
│   ├── IMPLEMENTATION_SUMMARY.md
│   ├── DEPENDENCIES.md         # Dependency information
│   ├── CHECKLIST.md
│   ├── DOCKER_README.md
│   └── DOCKER_SETUP.md
│
├── output/                     # Scan results (auto-generated)
│   └── (scan results)
│
├── payloads/                   # Attack payloads
│   ├── lfi-payloads.txt
│   ├── lfi.txt
│   ├── or.txt
│   ├── xss.txt
│   ├── xsspollygots.txt
│   └── sqli/
│       ├── generic.txt
│       ├── mysql.txt
│       ├── postgresql.txt
│       ├── oracle.txt
│       └── mssql.txt
│
├── reports/                    # Generated reports (auto-generated)
│   └── (HTML/JSON reports)
│
├── scripts/                    # Utility scripts
│   ├── start.sh                # Interactive startup script
│   ├── filter.sh               # Filter script
│   ├── docker-commands.sh      # Docker helper commands
│   ├── docker-pull.sh          # Pull Docker image
│   ├── docker-run.sh           # Run Docker container (Linux/Mac)
│   ├── docker-run.bat          # Run Docker container (Windows)
│   └── test-docker-setup.sh    # Docker setup testing
│
├── utils/                      # Utility modules
│   ├── __init__.py
│   ├── config.py               # Configuration management
│   └── platform_helper.py      # Cross-platform compatibility
│
├── web/                        # Web interface
│   ├── templates/
│   │   ├── index.html          # Dashboard
│   │   └── reports.html        # Report viewer
│   └── static/
│       └── js/
│           └── main.js         # Frontend JavaScript
│
├── .gitignore                  # Git exclusions
├── app.py                      # Flask web application entry point
├── main.py                     # CLI application entry point
├── docker compose.yml          # Symlink to .docker/docker compose.yml
├── requirements.txt            # Python dependencies (all)
├── requirements-docker.txt     # Docker-specific dependencies
├── requirements-gui.txt        # GUI-specific dependencies
├── requirements-lock.txt       # Pinned dependency versions
└── PROJECT_STRUCTURE.md        # This file
```

## File Descriptions

### Root Level Files

- **app.py**: Flask web application entry point (web GUI mode)
- **main.py**: CLI application entry point (terminal mode)
- **docker compose.yml**: Symlink for easy access to Docker Compose config

### Configuration Files

- **requirements.txt**: All Python dependencies (for local development)
- **requirements-docker.txt**: Docker-optimized dependencies (Linux compatible)
- **requirements-gui.txt**: Additional GUI-specific packages
- **requirements-lock.txt**: Pinned versions for reproducible builds

### Core Application (`core/`)

Contains the platform-independent scanning logic:
- Scanners (LFI, SQLi, XSS, OR, CRLF)
- Report generation
- Payload loading

### Web Interface (`web/`)

Modern web-based GUI:
- HTML templates with TailwindCSS
- JavaScript for real-time updates via Socket.IO
- Responsive design

### Utilities (`utils/`)

Helper modules:
- Configuration management
- Platform-specific helpers (Windows/Linux/macOS)
- Chrome/ChromeDriver path detection

### Documentation (`docs/`)

All project documentation:
- User guides
- API documentation
- Development workflows
- Docker setup instructions

### Scripts (`scripts/`)

Automation and helper scripts:
- Docker run scripts (cross-platform)
- Startup scripts
- Testing scripts

### Docker Configuration (`.docker/`)

Containerization files:
- Dockerfile: Multi-stage build, optimized image
- docker compose.yml: Service orchestration
- .dockerignore: Build exclusions

### Binaries (`bin/`)

Pre-compiled binaries:
- ChromeDriver for Linux
- Future: ChromeDriver for Windows/macOS

### Output Directories

- **output/**: Raw scan results (auto-generated)
- **reports/**: HTML/JSON reports (auto-generated)

## Development Workflow

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run CLI mode
python main.py

# Run web GUI
python app.py
```

### Docker Development
```bash
# Build and run
docker compose up raidscanner-web

# Or CLI mode
docker compose up raidscanner-cli
```

## Key Principles

1. **Separation of Concerns**: Core logic separate from UI
2. **Platform Independent**: Core modules work on any OS
3. **Docker First**: Containerized for portability
4. **Well Documented**: Comprehensive guides in docs/
5. **Standard Layout**: Follows Python project best practices

## Adding New Features

### New Scanner
1. Add scanner logic to `core/scanner_engine.py`
2. Add payloads to `payloads/`
3. Create API endpoint in `app.py` (web mode)
4. Add CLI option to `main.py` (CLI mode)

### New Web Page
1. Create HTML in `web/templates/`
2. Add static files to `web/static/`
3. Add route in `app.py`

### New Script
1. Add script to `scripts/`
2. Make executable: `chmod +x scripts/your-script.sh`
3. Document in `docs/`

## Build & Deployment

### Building Docker Image
```bash
docker compose build
```

### Running Services
```bash
# Web interface
docker compose up raidscanner-web

# CLI mode
docker compose up raidscanner-cli
```

### Publishing
```bash
# Tag image
docker tag raidscanner:latest zahidoverflow/raidscanner:v2.0

# Push to Docker Hub
docker push zahidoverflow/raidscanner:v2.0
```

## Notes

- Keep `docker compose.yml` symlink in root for user convenience
- All documentation goes in `docs/`
- All scripts go in `scripts/`
- Binary files go in `bin/`
- Core logic stays platform-independent
