from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        COMMENT ON COLUMN "callback_messages"."form_stage" IS 'AWAITING_ANSWER: awaiting_answer
DECLINED: declined
INVITATION_NEEDINESS_ASKED: invitation_neediness_asked
INVITATION_ADDRESS_INPUT: invitation_address_input
INVITATION_GEOTAG_VALIDATION: invitation_geotag_validation
INVITATION_ADDRESS_TEXT_INPUT: invitation_address_text_input
INVITATION_INFO_SPECIFICATION: invitation_info_specification
FILLING_ADDITIONAL_INFO: filling_additional_info
COMPLETED: completed';
        COMMENT ON COLUMN "commands"."form_stage" IS 'AWAITING_ANSWER: awaiting_answer
DECLINED: declined
INVITATION_NEEDINESS_ASKED: invitation_neediness_asked
INVITATION_ADDRESS_INPUT: invitation_address_input
INVITATION_GEOTAG_VALIDATION: invitation_geotag_validation
INVITATION_ADDRESS_TEXT_INPUT: invitation_address_text_input
INVITATION_INFO_SPECIFICATION: invitation_info_specification
FILLING_ADDITIONAL_INFO: filling_additional_info
COMPLETED: completed';
        ALTER TABLE "telegram_users" ALTER COLUMN "user_id" TYPE BIGINT USING "user_id"::BIGINT;
        COMMENT ON COLUMN "guests_forms"."stage" IS 'AWAITING_ANSWER: awaiting_answer
DECLINED: declined
INVITATION_NEEDINESS_ASKED: invitation_neediness_asked
INVITATION_ADDRESS_INPUT: invitation_address_input
INVITATION_GEOTAG_VALIDATION: invitation_geotag_validation
INVITATION_ADDRESS_TEXT_INPUT: invitation_address_text_input
INVITATION_INFO_SPECIFICATION: invitation_info_specification
FILLING_ADDITIONAL_INFO: filling_additional_info
COMPLETED: completed';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        COMMENT ON COLUMN "commands"."form_stage" IS 'AWAITING_ANSWER: awaiting_answer
DECLINED: declined
INVITATION_NEEDINESS_ASKED: invitation_neediness_asked
INVITATION_ADDRESS_INPUT: invitation_address_input
INVITATION_GEOTAG_VALIDATION: invitation_geotag_validation
INVITATION_ADDRESS_TEXT_INPUT: invitation_address_text_input
INVITATION_INFO_SPECIFICATION: invitation_info_specification
INVITATION_INFO_VALIDATION: invitation_info_validation
FILLING_ADDITIONAL_INFO: filling_additional_info
COMPLETED: completed';
        COMMENT ON COLUMN "guests_forms"."stage" IS 'AWAITING_ANSWER: awaiting_answer
DECLINED: declined
INVITATION_NEEDINESS_ASKED: invitation_neediness_asked
INVITATION_ADDRESS_INPUT: invitation_address_input
INVITATION_GEOTAG_VALIDATION: invitation_geotag_validation
INVITATION_ADDRESS_TEXT_INPUT: invitation_address_text_input
INVITATION_INFO_SPECIFICATION: invitation_info_specification
INVITATION_INFO_VALIDATION: invitation_info_validation
FILLING_ADDITIONAL_INFO: filling_additional_info
COMPLETED: completed';
        ALTER TABLE "telegram_users" ALTER COLUMN "user_id" TYPE INT USING "user_id"::INT;
        COMMENT ON COLUMN "callback_messages"."form_stage" IS 'AWAITING_ANSWER: awaiting_answer
DECLINED: declined
INVITATION_NEEDINESS_ASKED: invitation_neediness_asked
INVITATION_ADDRESS_INPUT: invitation_address_input
INVITATION_GEOTAG_VALIDATION: invitation_geotag_validation
INVITATION_ADDRESS_TEXT_INPUT: invitation_address_text_input
INVITATION_INFO_SPECIFICATION: invitation_info_specification
INVITATION_INFO_VALIDATION: invitation_info_validation
FILLING_ADDITIONAL_INFO: filling_additional_info
COMPLETED: completed';"""
