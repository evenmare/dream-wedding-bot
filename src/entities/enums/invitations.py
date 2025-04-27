"""Module contains enums for invitations entities."""

import enum


class InvitationRequestStageEnum(str, enum.Enum):
    """List of paper invitation request stages."""

    # 1. Ask about invitation neediness
    ASKED = 'asked'

    # 2.0. Rejected. Invitation is not needed
    REJECTED = 'rejected'

    # 2.1. Invitation is needed
    # 2.1.1. Address input (GeoInfo or Text)
    ADDRESS_INPUT = 'address_input'
    # 2.1.1.1 Geotag validation
    GEOTAG_VALIDATION = 'geotag_validation'
    # 2.1.1.1.1 Text input instead geotag (if geotag is incorrect)
    ADDRESS_TEXT_INPUT = 'address_text_input'

    # 2.1.2 (text input at first) | 2.1.1.2 (geotag is correct) | 2.1.1.1.2 (text input after incorrect geotag)
    INFO_SPECIFICATION = 'info_specification'

    # 2.1.3 | 2.1.1.3 | 2.1.1.1.3 Validation of full address
    VALIDATION = 'validation'

    # 2.1.4 | 2.1.1.4 | 2.1.1.1.4 Request completed
    COMPLETED = 'completed'
