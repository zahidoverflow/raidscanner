#!/bin/bash

# RaidScanner Docker Quick Commands
# Use this file as a reference for common Docker operations

echo "🔍 RaidScanner Docker Commands"
echo "================================"
echo ""

case "${1}" in
  build)
    echo "Building Docker image..."
    docker compose build
    ;;
  
  run)
    echo "Running RaidScanner..."
    docker compose run --rm raidscanner
    ;;
  
  shell)
    echo "Opening shell in container..."
    docker compose run --rm --entrypoint /bin/bash raidscanner
    ;;
  
  filter)
    echo "Running filter.sh script..."
    docker compose run --rm --entrypoint /bin/bash raidscanner -c "./filter.sh"
    ;;
  
  clean)
    echo "Cleaning up Docker resources..."
    docker compose down
    docker system prune -f
    ;;
  
  logs)
    echo "Showing container logs..."
    docker compose logs -f
    ;;
  
  update)
    echo "Rebuilding image (no cache)..."
    docker compose build --no-cache
    ;;
  
  *)
    echo "Usage: $0 {build|run|shell|filter|clean|logs|update}"
    echo ""
    echo "Commands:"
    echo "  build   - Build the Docker image"
    echo "  run     - Run RaidScanner interactively"
    echo "  shell   - Open bash shell in container"
    echo "  filter  - Run the filter.sh script"
    echo "  clean   - Remove containers and clean up"
    echo "  logs    - Show container logs"
    echo "  update  - Rebuild image from scratch"
    echo ""
    echo "Examples:"
    echo "  ./docker-commands.sh build"
    echo "  ./docker-commands.sh run"
    echo "  ./docker-commands.sh shell"
    ;;
esac
