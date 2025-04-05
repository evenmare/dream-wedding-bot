from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "guests" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "first_name" VARCHAR(16) NOT NULL,
    "last_name" VARCHAR(32) NOT NULL,
    "patronymic" VARCHAR(32),
    "phone_number" VARCHAR(12) NOT NULL,
    "birth_date" DATE NOT NULL
);
COMMENT ON TABLE "guests" IS 'Guest model.';
CREATE TABLE IF NOT EXISTS "guests_info" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "category" VARCHAR(8) NOT NULL,
    "is_resident" BOOL NOT NULL DEFAULT True,
    "is_transportation_needed" BOOL NOT NULL DEFAULT False,
    "is_registration_guest" BOOL NOT NULL DEFAULT False,
    "guest_id" INT NOT NULL UNIQUE REFERENCES "guests" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "guests_info"."category" IS 'RELATIVE: relative\nFRIEND: friend\nWITNESS: witness';
COMMENT ON TABLE "guests_info" IS 'Guest info model.';
CREATE TABLE IF NOT EXISTS "telegram_users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "username" VARCHAR(64),
    "guest_id" INT NOT NULL UNIQUE REFERENCES "guests" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "telegram_users" IS 'Telegram user model.';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
