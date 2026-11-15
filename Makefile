.PHONY: up down restart logs ps


COMPOSE = docker compose

.env:
	@cp .env.example .env

up: .env            ## build + start (сначала должен быть поднят dmavens-stat-cf)
	$(COMPOSE) up -d --build
	@set -a; . ./.env; set +a; echo "dashboard: http://localhost:$$PORT/"

down:
	$(COMPOSE) down

restart:            ## recreate app (re-reads .env)
	$(COMPOSE) up -d --force-recreate app

logs:
	$(COMPOSE) logs -f app

ps:
	$(COMPOSE) ps
