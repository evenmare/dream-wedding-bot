"""Module contains enums for invitations entities."""

import enum


class GuestFormStageEnum(str, enum.Enum):
    """List of paper invitation request stages."""

    AWAITING_ANSWER = 'awaiting_answer'
    DECLINED = 'declined'
    INVITATION_NEEDINESS_ASKED = 'invitation_neediness_asked'
    INVITATION_ADDRESS_INPUT = 'invitation_address_input'
    INVITATION_GEOTAG_VALIDATION = 'invitation_geotag_validation'
    INVITATION_ADDRESS_TEXT_INPUT = 'invitation_address_text_input'
    INVITATION_INFO_SPECIFICATION = 'invitation_info_specification'
    INVITATION_INFO_VALIDATION = 'invitation_info_validation'
    FILLING_ADDITIONAL_INFO = 'filling_additional_info'
    COMPLETED = 'completed'
