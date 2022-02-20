from json import JSONDecodeError
from typing import Optional

import requests

from .exceptions import HTTPException


class HoneygainHTTP:
    API_VERSION = 1

    BASE_URL = 'https://dashboard.honeygain.com/api/v{version}'
    USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0'

    def __init__(self):
        self._token: Optional[str] = None
        self._sess: Optional[requests.Session] = None

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self._token = value
        self._sess.headers.update({
            'Authorization': 'Bearer ' + self.token
        })

    def prepare(self):
        """
        Reset our session so we can log in again.
        """
        self._sess = requests.Session()
        self._sess.headers.update({
            'User-Agent': self.USER_AGENT,
            'Referer': 'https://dashboard.honeygain.com/'
        })

    @property
    def is_logged_in(self):
        """
        Checks whether we are currently logged in
        :return: If we have a token set
        """
        return self._token is not None

    def request(self, method, endpoint, json=None, params=None, version=API_VERSION) -> dict:
        if self._sess is None:
            raise RuntimeError('Session not set up yet')

        url = self.BASE_URL.format(version=version) + endpoint
        try:
            r = self._sess.request(method, url, json=json, params=params)
        except requests.HTTPError as ex:
            raise HTTPException(f'Error while calling API: {ex.strerror}')

        if r.status_code == 201:
            return {}

        try:
            data = r.json()
        except JSONDecodeError:
            raise HTTPException('Could not parse API response data')

        if not r.ok:
            error_str = data.get('details')
            raise HTTPException(f'HTTP Error {r.status_code}: {error_str}')

        return data

    def get_token(self, email, password) -> str:
        payload = {'email': email, 'password': password}
        resp = self.request('POST', '/users/tokens', json=payload)

        return resp.get('data', dict()).get('access_token')

    def get_me(self) -> dict:
        return self.request('GET', '/users/me')

    def get_devices(self) -> dict:
        return self.request('GET', '/devices', version=2)

    def get_tos(self) -> dict:
        return self.request('GET', '/users/tos')

    def get_notifications(self, user_id: int) -> dict:
        return self.request('GET', '/notifications', params={'user_id': user_id})

    def claim_credits(self, notif_id: str, campaign_id: str, user_id: str) -> dict:
        endpoint = f'/notifications/{notif_id}/actions'
        payload = {
            'campaign_id': campaign_id,
            'user_id': user_id,
            'action': 'triggered'
        }
        return self.request('POST', endpoint, json=payload)

    def check_credits_claimed(self) -> dict:
        return self.request('POST', '/contest_winnings')

    def get_stats(self) -> dict:
        return self.request('GET', '/earnings/stats')

    def get_jt_stats(self) -> dict:
        return self.request('GET', '/jt-earnings/stats')

    def get_earnings_today(self) -> dict:
        return self.request('GET', '/earnings/today')

    def get_jt_earnings_today(self) -> dict:
        return self.request('GET', '/jt-earnings/today')

    def get_referral_earnings(self) -> dict:
        return self.request('GET', '/referrals/earnings')

    def get_balance(self) -> dict:
        return self.request('GET', '/users/balances')

    def get_jt_balance(self) -> dict:
        return self.request('GET', '/earnings/jt')

    def get_wallet_stats(self) -> dict:
        return self.request('GET', '/earnings/wallet-stats')
