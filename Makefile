COMPOSE_FILE = docker-compose.yml

# Build and start the services
.PHONY: up
up:
	docker-compose -f $(COMPOSE_FILE) up -d --build

# Stop the services
.PHONY: down
down:
	docker-compose -f $(COMPOSE_FILE) down

# Restart the services
.PHONY: restart
restart: down up

# View the logs
.PHONY: logs
logs:
	docker-compose -f $(COMPOSE_FILE) logs -f

# Clean up the services (remove containers, networks, volumes, and images created by up)
.PHONY: clean
clean:
	docker-compose -f $(COMPOSE_FILE) down -v --rmi all

# Show the status of the services
.PHONY: status
status:
	docker-compose -f $(COMPOSE_FILE) ps

# Prune unused Docker images
.PHONY: prune
prune:
	docker image prune -f