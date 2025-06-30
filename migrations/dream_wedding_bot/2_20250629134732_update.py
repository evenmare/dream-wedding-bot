from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "callback_messages" ADD "notification_id" INT UNIQUE;
        CREATE TABLE IF NOT EXISTS "notifications" (
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "notification_id" SERIAL NOT NULL PRIMARY KEY,
    "code" VARCHAR(16) NOT NULL UNIQUE,
    "is_personal" BOOL NOT NULL DEFAULT True
);
COMMENT ON TABLE "notifications" IS 'Model for storing notification info.';
        CREATE TABLE IF NOT EXISTS "personal_notifications" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_sent" BOOL NOT NULL DEFAULT False,
    "guest_id" INT NOT NULL REFERENCES "guests" ("guest_id") ON DELETE CASCADE,
    "notification_id" INT NOT NULL REFERENCES "notifications" ("notification_id") ON DELETE CASCADE
);
COMMENT ON TABLE "personal_notifications" IS 'Model for storing available notifications for Guest.';
        ALTER TABLE "callback_messages" ADD CONSTRAINT "fk_callback_notifica_df818c72" FOREIGN KEY ("notification_id") REFERENCES "notifications" ("notification_id") ON DELETE SET NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "callback_messages" DROP CONSTRAINT IF EXISTS "fk_callback_notifica_df818c72";
        DROP TABLE IF EXISTS "personal_notifications";
        ALTER TABLE "callback_messages" DROP COLUMN "notification_id";
        DROP TABLE IF EXISTS "personal_notifications";
        DROP TABLE IF EXISTS "notifications";"""
