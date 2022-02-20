from typing import Optional

from pydantic import parse_obj_as

from .exceptions import ClientException
from .http import HoneygainHTTP
from .schemas import UserProfile, Device, TermsOfService, \
    Notification, ReferralEarnings, TodayStats, DailyStats, \
    Balance, HoneygainBalance, WalletStats


def _requires_login(func):
    def wrapper(*args, **kwargs):
        # self is accessible because it's called from a Client instance
        if not args[0].http.is_logged_in:
            raise ClientException('You must log in first.')

        return func(*args, **kwargs)

    return wrapper


class Client:
    def __init__(self):
        """
        A Client that communicates with the HoneyGain API.
        """
        self.http = HoneygainHTTP()
        self._user_id = None

    def _get_honeypot_notif(self) -> Optional[Notification]:
        notifications = self.get_notifications()
        return next((n for n in notifications
                     if n.template == 'lucky_pot'), None)

    @property
    def token(self):
        return self.http.token

    @token.setter
    def token(self, account_token):
        if self.http.is_logged_in:
            raise ClientException('You must logout first')

        self.http.prepare()
        self.http.token = account_token

    @property
    def can_claim_credits(self):
        return self._get_honeypot_notif() is not None

    def login(self, email, password):
        if self.http.is_logged_in:
            raise ClientException('You must logout first')

        # Clean up session and fetch our token
        self.http.prepare()
        token = self.http.get_token(email, password)
        self.token = token

    @_requires_login
    def get_profile(self) -> UserProfile:
        data = self.http.get_me().get('data')
        self._user_id = data.get('id')  # store this for notifications

        return UserProfile(**data)

    @_requires_login
    def get_devices(self):
        data = self.http.get_devices().get('data')
        return parse_obj_as(list[Device], data)

    @_requires_login
    def get_tos(self) -> TermsOfService:
        data = self.http.get_tos().get('data')
        return TermsOfService(**data)

    @_requires_login
    def get_notifications(self) -> list[Notification]:
        if self._user_id is None:  # populate user ID first
            self.get_profile()

        data = self.http.get_notifications(self._user_id).get('data')
        return parse_obj_as(list[Notification], data)

    @_requires_login
    def claim_credits(self) -> float:
        # this should also populate self._user_id through get_notifications
        notif = self._get_honeypot_notif()
        if notif is None:
            raise ClientException('Honeypot cannot be claimed yet!')

        self.http.claim_credits(notif.hash, notif.campaign_id, self._user_id)
        resp = self.http.check_credits_claimed()

        return resp.get('data', {}).get('credits')

    @_requires_login
    def get_monthly_stats(self) -> list[DailyStats]:
        data = self.http.get_stats()
        parsed: list[dict] = [{'date': k, **v} for k, v in data.items()]

        return parse_obj_as(list[DailyStats], parsed)

    @_requires_login
    def get_jt_monthly_stats(self) -> list[DailyStats]:
        data = self.http.get_jt_stats()
        parsed: list[dict] = [{'date': k, **v} for k, v in data.items()]

        return parse_obj_as(list[DailyStats], parsed)

    @_requires_login
    def get_today_earnings(self) -> TodayStats:
        data = self.http.get_earnings_today()
        return TodayStats(**data)

    @_requires_login
    def get_jt_today_earnings(self) -> TodayStats:
        data = self.http.get_jt_earnings_today()
        return TodayStats(**data)

    @_requires_login
    def get_referral_earnings(self) -> ReferralEarnings:
        data = self.http.get_referral_earnings()
        return ReferralEarnings(**data)

    @_requires_login
    def get_balance(self) -> HoneygainBalance:
        data = self.http.get_balance().get('data')
        return HoneygainBalance(**data)

    @_requires_login
    def get_jt_balance(self) -> Balance:
        data = self.http.get_jt_balance().get('data')
        return Balance(**data)

    @_requires_login
    def get_wallet_stats(self) -> list[WalletStats]:
        data = self.http.get_wallet_stats().get('data')
        parsed: list[dict] = [{'date': k, **v} for k, v in data.items()]

        return parse_obj_as(list[WalletStats], parsed)
