from typing import Optional

from pydantic import model_validator

from settings_models._combat import SettingsModel, Field


class IntercomSettings(SettingsModel):
    """
    Settings for intercom on kiosk devices
    """
    enabled: bool = Field(..., description="If intercom enabled on kiosk devices")
    phone_number: Optional[str] = Field(None, description="Phone number for intercom emergency calls")

    @model_validator(mode="after")
    def data_validation(cls, values):
        if values.enabled and values.phone_number is None:
            raise ValueError("phone_number must be set if intercom is enabled")
        return values
