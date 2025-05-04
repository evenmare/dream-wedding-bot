from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "callback_messages" (
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "callback_message_id" SERIAL NOT NULL PRIMARY KEY,
    "form_stage" VARCHAR(32),
    "command" VARCHAR(32),
    "text_filepath" VARCHAR(64) NOT NULL,
    "image_filepath" VARCHAR(64)
);
COMMENT ON COLUMN "callback_messages"."form_stage" IS 'AWAITING_ANSWER: awaiting_answer\nDECLINED: declined\nINVITATION_NEEDINESS_ASKED: invitation_neediness_asked\nINVITATION_ADDRESS_INPUT: invitation_address_input\nINVITATION_GEOTAG_VALIDATION: invitation_geotag_validation\nINVITATION_ADDRESS_TEXT_INPUT: invitation_address_text_input\nINVITATION_INFO_SPECIFICATION: invitation_info_specification\nINVITATION_INFO_VALIDATION: invitation_info_validation\nCOMPLETED: completed';
COMMENT ON COLUMN "callback_messages"."command" IS 'START: start\nCEREMONY_INFO: ceremony_info\nREGISTRATION_INFO: registration_info';
COMMENT ON TABLE "callback_messages" IS 'Model for storing message content for callbacks.';
CREATE TABLE IF NOT EXISTS "guests" (
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "guest_id" SERIAL NOT NULL PRIMARY KEY,
    "first_name" VARCHAR(16) NOT NULL,
    "last_name" VARCHAR(32) NOT NULL,
    "patronymic" VARCHAR(32),
    "phone_number" VARCHAR(12) NOT NULL,
    "birth_date" DATE NOT NULL,
    "gender" VARCHAR(1) NOT NULL,
    "category" VARCHAR(8) NOT NULL,
    "is_resident" BOOL NOT NULL DEFAULT True,
    "is_registration_guest" BOOL NOT NULL DEFAULT False
);
CREATE INDEX IF NOT EXISTS "idx_guests_phone_n_10f71e" ON "guests" ("phone_number");
COMMENT ON COLUMN "guests"."gender" IS 'FEMALE: F\nMALE: M';
COMMENT ON COLUMN "guests"."category" IS 'RELATIVE: relative\nFRIEND: friend\nWITNESS: witness';
COMMENT ON TABLE "guests" IS 'Guest model.';
CREATE TABLE IF NOT EXISTS "guests_forms" (
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "stage" VARCHAR(32) NOT NULL,
    "guest_id" INT NOT NULL PRIMARY KEY REFERENCES "guests" ("guest_id") ON DELETE RESTRICT
);
COMMENT ON COLUMN "guests_forms"."stage" IS 'AWAITING_ANSWER: awaiting_answer\nDECLINED: declined\nINVITATION_NEEDINESS_ASKED: invitation_neediness_asked\nINVITATION_ADDRESS_INPUT: invitation_address_input\nINVITATION_GEOTAG_VALIDATION: invitation_geotag_validation\nINVITATION_ADDRESS_TEXT_INPUT: invitation_address_text_input\nINVITATION_INFO_SPECIFICATION: invitation_info_specification\nINVITATION_INFO_VALIDATION: invitation_info_validation\nCOMPLETED: completed';
COMMENT ON TABLE "guests_forms" IS 'Guest form information.';
CREATE TABLE IF NOT EXISTS "invitations_requests" (
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "address" TEXT,
    "address_specification" TEXT,
    "guest_id" INT NOT NULL PRIMARY KEY REFERENCES "guests" ("guest_id") ON DELETE RESTRICT
);
COMMENT ON TABLE "invitations_requests" IS 'Invitation request model.';
CREATE TABLE IF NOT EXISTS "telegram_users" (
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT NOT NULL PRIMARY KEY,
    "username" VARCHAR(64),
    "guest_id" INT NOT NULL UNIQUE REFERENCES "guests" ("guest_id") ON DELETE CASCADE
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
