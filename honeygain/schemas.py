from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, Field


#
# Profile related
#
class UserProfile(BaseModel):
    """
    Represents a user's profile and associated data.
    """
    id: str
    email: str
    status: str

    jumptask_mode: bool = Field(False, alias='jt_toggle')

    total_device_count: int = Field(alias='total_devices')
    active_device_count: int = Field(alias='active_devices_count')

    email_confirmed: bool
    referral_code: str
    created_at: datetime
    features: list[str]


class TermsOfService(BaseModel):
    """
    Represents a ToS object with acceptance data.
    """
    version: str
    status: str
    accepted_at: date = Field(alias='first_terms_accepted_at')


#
# Statistics
#
class CreditStats(BaseModel):
    """
    A generic credit stat entry
    """
    credits: int


class GatheringStats(CreditStats):
    """
    A single gathering stats entry
    """
    traffic: int


class CDNStats(CreditStats):
    """
    A single content delivery network stats entry
    """
    time: int


class DailyStats(BaseModel):
    """
    Represents a daily stats entry.
    """
    date: date

    gathering: GatheringStats  # credits + traffic
    content_delivery: CDNStats  # credits + time
    referrals: CreditStats  # credits
    winnings: CreditStats  # credits
    other: CreditStats  # credits
    bonus: Optional[CreditStats]  # credits
