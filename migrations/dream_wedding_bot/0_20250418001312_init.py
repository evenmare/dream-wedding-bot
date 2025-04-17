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
    "birth_date" DATE NOT NULL,
    "category" VARCHAR(8) NOT NULL,
    "is_resident" BOOL NOT NULL DEFAULT True,
    "is_registration_guest" BOOL NOT NULL DEFAULT False,
    "status" VARCHAR(16)
);
CREATE INDEX IF NOT EXISTS "idx_guests_phone_n_10f71e" ON "guests" ("phone_number");
COMMENT ON COLUMN "guests"."category" IS 'RELATIVE: relative\nFRIEND: friend\nWITNESS: witness';
COMMENT ON COLUMN "guests"."status" IS 'INVITED: invited\nAWAITING_ANSWER: awaiting_answer\nDECLINED: declined\nCONFIRMED: confirmed';
COMMENT ON TABLE "guests" IS 'Guest model.';
CREATE TABLE IF NOT EXISTS "invitations_requests" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "stage" VARCHAR(32) NOT NULL,
    "address" TEXT,
    "address_specification" TEXT,
    "guest_id" INT NOT NULL UNIQUE REFERENCES "guests" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "invitations_requests"."stage" IS 'ASKED: asked\nREJECTED: rejected\nADDRESS_INPUT: address_input\nGEOTAG_VALIDATION: geotag_validation\nADDRESS_TEXT_INPUT: address_text_input\nINFO_SPECIFICATION: info_specification\nVALIDATION: validation\nCOMPLETED: completed';
COMMENT ON TABLE "invitations_requests" IS 'Invitation request model.';
CREATE TABLE IF NOT EXISTS "telegram_users" (
    "id" INT NOT NULL PRIMARY KEY,
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
