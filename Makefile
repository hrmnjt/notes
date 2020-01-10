DC_COMPOSE = docker-compose --project-name notes-docs -f setup/docker-compose.yml

start-docs-server:
	@$(DC_COMPOSE) up --timeout 0 --renew-anon-volumes --force-recreate --always-recreate-deps --remove-orphans --detach
	@echo "Docs are available at localhost:8000"

stop-docs-server:
	@$(DC_COMPOSE) down --timeout 0

clean-docs-server:
	@$(DC_COMPOSE) down --volumes --timeout 0 --remove-orphans
	@docker container prune -f
	@docker volume prune -f
	@docker container ls -a
	@docker volume ls
