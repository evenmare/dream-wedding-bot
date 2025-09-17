run_infrastructures:
	docker compose up -d db redis migrations

make_migration: run_infrastructures
	@read -p "Enter Migration Name: " migration_name; \
	docker compose exec migrations uv run aerich --app dream_wedding_bot migrate --name $$migration_name

make_empty_migration: run_infrastructures
	@read -p "Enter Migration Name: " migration_name; \
	docker compose exec migrations uv run aerich --app dream_wedding_bot migrate --name $$migration_name --empty

migrate: run_infrastructures
	docker compose up -d migrations

downgrade: run_infrastructures
	docker compose exec migrations uv run aerich --app dream_wedding_bot downgrade

update_venv:
	uv sync --group dev --locked

prepare_env:
	cp .env.example .env

init: prepare_env update_venv run_infrastructures migrate
	uv tool install pre-commit
	uv tool install ruff
	uvx pre-commit install
