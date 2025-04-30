"""Module contains enums for invitations entities."""

import enum


class GuestFormStageEnum(str, enum.Enum):
    """List of paper invitation request stages."""

    INVITED = 'invited'
    AWAITING_ANSWER = 'awaiting_answer'
    DECLINED = 'declined'
    CONFIRMED = 'confirmed'

    # 1. Ask about invitation neediness
    INVITATION_NEEDINESS_ASKED = 'invitation_neediness_asked'

    # 2.1. Invitation is needed
    # 2.1.1. Address input (GeoInfo or Text)
    INVITATION_ADDRESS_INPUT = 'invitation_address_input'
    # 2.1.1.1 Geotag validation
    INVITATION_GEOTAG_VALIDATION = 'invitation_geotag_validation'
    # 2.1.1.1.1 Text input instead geotag (if geotag is incorrect)
    INVITATION_ADDRESS_TEXT_INPUT = 'invitation_address_text_input'

    # 2.1.2 (text input at first) | 2.1.1.2 (geotag is correct) | 2.1.1.1.2 (text input after incorrect geotag)
    INVITATION_INFO_SPECIFICATION = 'invitation_info_specification'

    # 2.1.3 | 2.1.1.3 | 2.1.1.1.3 Validation of full address
    INVITATION_INFO_VALIDATION = 'invitation_info_validation'

    # 2.0 (invitation is not needed) | 2.1.4 | 2.1.1.4 | 2.1.1.1.4 Request completed
    COMPLETED = 'completed'
