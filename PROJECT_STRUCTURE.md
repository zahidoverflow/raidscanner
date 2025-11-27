# RaidScanner Project Structure

## Directory Layout

```
raidscanner/
├── .docker/                    # Docker configuration
│   ├── Dockerfile              # Container build definition
│   ├── compose.yml             # Docker Compose configuration (V2)
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
│   ├── README.md               # Complete user documentation
│   ├── WEB_GUI.md              # Web interface guide
│   ├── DOCKER.md               # Docker deployment guide
│   ├── QUICKSTART.md           # 5-minute quick start
│   ├── ARCHITECTURE.md         # System design & architecture
│   └── IMPLEMENTATION_SUMMARY.md  # Development summary
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
├── README.md                   # Main project README (GitHub landing page)
├── app.py                      # Flask web application entry point
├── main.py                     # CLI application entry point
├── compose.yml                 # Symlink to .docker/compose.yml
├── requirements.txt            # Python dependencies (all)
├── requirements-docker.txt     # Docker-specific dependencies
├── requirements-gui.txt        # GUI-specific dependencies
├── requirements-lock.txt       # Pinned dependency versions
└── PROJECT_STRUCTURE.md        # This file - project organization guide
```

## Documentation Structure

### Root Level
- **README.md**: Main project documentation - installation, usage, features (GitHub landing page)
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

Comprehensive project documentation:
- **README.md**: Complete user documentation with all features
- **QUICKSTART.md**: 5-minute quick start guide
- **WEB_GUI.md**: Web interface guide and API reference
- **DOCKER.md**: Complete Docker deployment guide
- **ARCHITECTURE.md**: System design and components
- **IMPLEMENTATION_SUMMARY.md**: Development history

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

## Common Commands Reference

### Quick Start
```bash
# Web GUI (Recommended)
docker compose up -d raidscanner-web    # Start in background
# Access: http://localhost:5000

# CLI Mode
docker compose run --rm raidscanner-cli  # Interactive terminal

# Both Services
docker compose up -d                     # Start all services
```

### Docker Compose Commands
```bash
# Service Management
docker compose up -d raidscanner-web     # Start web (background)
docker compose up raidscanner-cli        # Start CLI (foreground)
docker compose down                      # Stop all services
docker compose restart raidscanner-web   # Restart web service

# Logs & Monitoring
docker compose logs -f raidscanner-web   # Follow web logs
docker compose logs --tail=100           # Last 100 log lines
docker compose ps                        # List running services

# Building & Updating
docker compose build                     # Build images
docker compose build --no-cache          # Rebuild from scratch
docker compose pull                      # Pull latest images

# Cleanup
docker compose down --volumes            # Remove volumes
docker compose down --rmi all            # Remove images
```

### Direct Docker Commands
```bash
# Pull from Docker Hub
docker pull zahidoverflow/raidscanner:latest

# Run Web GUI
docker run -d -p 5000:5000 \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/reports:/app/reports \
  --shm-size=2g \
  --name raidscanner-web \
  zahidoverflow/raidscanner:latest

# Run CLI
docker run -it --rm \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/reports:/app/reports \
  --shm-size=2g \
  zahidoverflow/raidscanner:latest

# Container Management
docker ps                                # List running containers
docker stop raidscanner-web              # Stop container
docker rm raidscanner-web                # Remove container
docker logs -f raidscanner-web           # View logs
```

### Helper Scripts
```bash
# Linux/Mac
chmod +x scripts/docker-run.sh
./scripts/docker-run.sh

# Windows
scripts\docker-run.bat
```

### Development Workflow

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
# Build and run web GUI
docker compose up -d raidscanner-web

# Or CLI mode
docker compose run --rm raidscanner-cli

# View logs
docker compose logs -f

# Rebuild after changes
docker compose build --no-cache
```

## Quick Reference URLs

| Resource | URL |
|----------|-----|
| Web GUI | http://localhost:5000 |
| Reports | http://localhost:5000/reports |
| Docker Hub | https://hub.docker.com/r/zahidoverflow/raidscanner |
| GitHub | https://github.com/zahidoverflow/raidscanner |
| Documentation | See `docs/` directory |

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
