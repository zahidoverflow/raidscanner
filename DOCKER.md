# 🐳 Docker Deployment - IST Vulnerable Web App

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Build and start the container
docker compose up -d

# Access the app
http://localhost:3000
```

### Using Docker CLI

```bash
# Build the image
docker build -t ist-vulnerable-webapp:latest .

# Run the container
docker run -d -p 3000:80 --name ist-webapp ist-vulnerable-webapp:latest

# Access the app
http://localhost:3000
```

---

## Docker Configuration

### Multi-Stage Build

**Stage 1: Builder (Node 20 Alpine)**
- Installs dependencies
- Builds the Vite application
- Optimizes for production

**Stage 2: Production (Nginx 1.25 Alpine)**
- Serves static files
- Lightweight (~50MB final image)
- Non-root user for security
- Health checks enabled

### Features

✅ **Multi-stage build** - Smaller final image  
✅ **Alpine Linux** - Minimal base image  
✅ **Non-root user** - Enhanced security  
✅ **Health checks** - Container monitoring  
✅ **Gzip compression** - Faster loading  
✅ **Security headers** - XSS protection  
✅ **Resource limits** - CPU and memory caps  
✅ **SPA routing** - Client-side routing support  

---

## Docker Commands

### Build

```bash
# Build the image
docker compose build

# Build with no cache
docker compose build --no-cache

# Build and tag
docker build -t ist-vulnerable-webapp:v1.0 .
```

### Run

```bash
# Start in detached mode
docker compose up -d

# Start with logs
docker compose up

# Start specific service
docker compose up vulnerable-webapp
```

### Stop

```bash
# Stop containers
docker compose down

# Stop and remove volumes
docker compose down -v

# Stop and remove images
docker compose down --rmi all
```

### Logs

```bash
# View logs
docker compose logs

# Follow logs
docker compose logs -f

# View last 100 lines
docker compose logs --tail=100
```

### Health Check

```bash
# Check container health
docker compose ps

# Manual health check
curl http://localhost:3000/health
```

---

## NPM Scripts

```bash
# Build Docker image
npm run docker:build

# Start container
npm run docker:up

# Stop container
npm run docker:down

# View logs
npm run docker:logs

# Restart container
npm run docker:restart
```

---

## Configuration

### Port Mapping

Default: `3000:80` (host:container)

**Change port**:
```yaml
# docker-compose.yml
ports:
  - "8080:80"  # Use port 8080 instead
```

### Resource Limits

```yaml
deploy:
  resources:
    limits:
      cpus: '0.5'      # Max 0.5 CPU cores
      memory: 256M     # Max 256MB RAM
    reservations:
      memory: 128M     # Min 128MB RAM
```

### Environment Variables

```yaml
environment:
  - NODE_ENV=production
  - CUSTOM_VAR=value
```

---

## Testing with RaidScanner

### Step 1: Start Vulnerable App

```bash
# In lab branch
docker compose up -d

# Verify it's running
curl http://localhost:3000/health
```

### Step 2: Run RaidScanner

```bash
# Switch to main branch
git checkout main

# Run scanner against local Docker container
docker compose run --rm raidscanner

# Test URLs:
# http://host.docker.internal:3000/notices?file=test.txt
# http://172.17.0.1:3000/notices?file=test.txt
```

**Note**: Use `host.docker.internal` (Windows/Mac) or `172.17.0.1` (Linux) to access host from container.

---

## Troubleshooting

### Issue: Port already in use

```bash
# Check what's using port 3000
netstat -ano | findstr :3000

# Change port in docker-compose.yml
ports:
  - "3001:80"
```

### Issue: Build fails

```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker compose build --no-cache
```

### Issue: Container not healthy

```bash
# Check container logs
docker compose logs vulnerable-webapp

# Check health status
docker inspect ist-vulnerable-webapp | grep Health

# Manual health check
curl http://localhost:3000/health
```

### Issue: Can't access from host

```bash
# Check container is running
docker compose ps

# Check port mapping
docker port ist-vulnerable-webapp

# Test from inside container
docker exec ist-vulnerable-webapp curl http://localhost/health
```

---

## Production Deployment

### Build for Production

```bash
# Build optimized image
docker build -t ist-vulnerable-webapp:prod .

# Tag for registry
docker tag ist-vulnerable-webapp:prod username/ist-vulnerable-webapp:latest

# Push to Docker Hub
docker push username/ist-vulnerable-webapp:latest
```

### Run in Production

```bash
# Pull from registry
docker pull username/ist-vulnerable-webapp:latest

# Run with restart policy
docker run -d \
  -p 80:80 \
  --name ist-webapp \
  --restart unless-stopped \
  username/ist-vulnerable-webapp:latest
```

---

## Security Considerations

### Non-Root User

Container runs as user `nginx-app` (UID 1001), not root.

### Security Headers

```nginx
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
```

### Resource Limits

Prevents container from consuming excessive resources.

### Health Checks

Automatically restarts unhealthy containers.

---

## Image Size

```
REPOSITORY                TAG       SIZE
ist-vulnerable-webapp     latest    ~50MB
```

**Breakdown**:
- Nginx Alpine: ~25MB
- Built app: ~15MB
- Dependencies: ~10MB

---

## Comparison: Docker vs Vercel

| Feature | Docker (Local) | Vercel (Cloud) |
|---------|---------------|----------------|
| **Deployment** | Manual | Auto (on push) |
| **Cost** | Free | Free tier |
| **Speed** | Instant | ~30 seconds |
| **Control** | Full | Limited |
| **Rate Limits** | None | Yes |
| **Best For** | Development, Testing | Production, Demo |

---

## Next Steps

1. ✅ Build Docker image: `docker compose build`
2. ✅ Start container: `docker compose up -d`
3. ✅ Test locally: `http://localhost:3000`
4. ✅ Test with scanner: Use `host.docker.internal:3000`
5. ✅ Deploy to Vercel: `git push origin lab`

---

**Status**: ✅ Dockerized with modern best practices!
