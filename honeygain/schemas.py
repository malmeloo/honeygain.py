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


class DeviceStats(BaseModel):
    """
    Simple stats for a device.
    """
    total_traffic: int
    total_credits: float
    streaming_seconds: int


class Device(BaseModel):
    """
    Represents an active device connected to your Honeygain account.
    """
    id: str
    name: str = Field(alias='model')
    platform: str
    version: str
    streaming_enabled: bool

    ip: str
    status: str
    last_active_time: datetime
    stats: DeviceStats


class Notification(BaseModel):
    """
    Represents a user's (unread) notifications.
    """
    campaign_id: str
    template: str
    priority: int

    hash: str
    title: str
    body: str


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
    traffic: int = Field(alias='bytes')

    class Config:
        """
        Pydantic config to allow multiple aliases
        """
        allow_population_by_field_name = True


class CDNStats(CreditStats):
    """
    A single content delivery network stats entry
    """
    time: int = Field(alias='seconds')

    class Config:
        """
        Pydantic config to allow multiple aliases
        """
        allow_population_by_field_name = True


class GenericStats(BaseModel):
    """
    Generic stats entry. Could be for any time period.
    """
    total: Optional[CreditStats]  # credits
    referrals: CreditStats = Field(alias='referral')  # credits
    winnings: CreditStats = Field(alias='winning')  # credits
    other: CreditStats  # credits
    bonus: Optional[CreditStats]  # credits

    gathering: GatheringStats  # credits + traffic
    content_delivery: CDNStats = Field(alias='cdn')  # credits + time

    class Config:
        """
        Pydantic config to allow multiple aliases
        """
        allow_population_by_field_name = True


class TodayStats(GenericStats):
    """
    Stats for the current day up until the current time.
    This only exists for people to distinguish TodayStats from DailyStats.
    """
    pass


class DailyStats(GenericStats):
    """
    Represents a daily stats entry.
    """
    date: date


#
# Balances
#
class Balance(BaseModel):
    """
    Represents a balance for any period of time.
    Does not have to be account balance; for example, this object is
    also used in the minimum payout field for HoneygainBalance.

    Bonus credits/cents will always be 0 for normal mode.
    """
    credits: float = Field(alias='total_credits')
    bonus_credits: Optional[float] = 0
    usd_cents: int = Field(alias='total_usd_cents')
    bonus_usd_cents: Optional[int] = 0

    class Config:
        """
        Pydantic config to allow multiple aliases
        """
        allow_population_by_field_name = True


class HoneygainBalance(BaseModel):
    """
    Contains multiple Balance objects with information about
    the current day, lifetime and minimum payout threshold.
    """
    today: Balance = Field(alias='realtime')
    lifetime: Balance = Field(alias='payout')
    min_payout: Balance


class WalletStats(BaseModel):
    """
    Daily stats split up into Honeygain and JumpTask mode.
    """
    date: date

    hg_credits: float
    jt_credits: float


#
# Misc earnings
#
class ReferralEarnings(BaseModel):
    """
    Account earnings and other data from referrals.
    """
    count: int
    total_earnings: float
    average_earnings: float
    first_referrals: list[str]
