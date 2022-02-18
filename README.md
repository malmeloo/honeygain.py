# Honeygain.py

A python wrapper to interact with Honeygain's API.

## Installation

```shell
$ coming soon...
zsh: command not found: coming
```

## Usage

```python
import honeygain
from honeygain.schemas import UserProfile

EMAIL = 'mike@example.com'
PASS = 'V3ryZ3cUReP@sSw0rD'  # TODO: remove my totally real password

# log in...
client = honeygain.Client()
client.login(EMAIL, PASS)

# alternatively, if you already have a token:
# client.token = 'myAccessToken'

profile: UserProfile = client.get_profile()
print(f'--- Logged in as {profile.email} ---')
print(f'Created at:       {profile.created_at}')
print(f'JumpTask enabled: {profile.jumptask_mode}')
print(f'Active devices:   {profile.active_device_count} / {profile.total_device_count}')
```

## A note about logging in

Due to the way this library works, running the above example will generate a new access token every time it's ran.
Because of this, it is **HEAVILY** recommended that you *store* the access token somewhere and cache it so you do not
have to call login() over and over.

Honeygain has set a very tight ratelimit on how often you can call the login endpoint, and they **WILL** prevent you
from logging in again after a couple tries. When this happens, you are effectively locked out of your account and will
have to try again the next day. That is, unless you have cached your access token like the smart person you are.

A very simple example to cache access tokens:

```python
import honeygain

client = honeygain.Client()

# getting a stored access token
with open('token.txt', 'r') as file:
    client.token = file.read().strip()

# storing an access token after logging in
with open('token.txt', 'w+') as file:
    file.write(client.token)
```

Access tokens last for a very long time. If your token has expired, the API will tell you by raising
a `honeygain.HTTPException`.

### If you do get yourself locked out

Two options:

1. Accept defeat. Your code is bad and you should feel bad. Try again tomorrow, or in an hour if you're lucky.
2. If you are still logged in on a web browser:
    1. Open the honeygain dashboard
    2. Open devtools -> storage -> local storage
    3. Your token is listed under the `JWT` key for the dashboard domain.

## Implemented endpoints

The base URL for all endpoints is `https://dashboard.honeygain.com/api/v{version}`. Version is 1 unless otherwise noted.

<details open>
<summary>General account</summary>

- [x] `POST /users/tokens` - Logging in with email + password
- [x] `GET /users/me` - Account details
- [x] `GET /users/tos` - ToS statistics
- [x] `GET /devices` - Currently active devices and stats about them.
  **Note:** uses API v2.

</details>


<details open>
<summary>Notifications</summary>

- [ ] `GET /notifications?user_id=<user id>` Get your notifications (why is there a user ID here??)
- [ ] `POST /notifications/<notif ID>/actions` Interact with the notification
- [ ] `GET /contest_winnings` Get the winnings of a contest. Can only be called after interacting with the notification
  as above.

</details>


<details open>
<summary>Lifetime earnings</summary>

- [x] `GET /earnings/jt` - Lifetime earnings in JumpTask mode
- [x] `GET /users/balances` - Lifetime earnings for "normal" mode, as well as the minimum payout threshold
- [x] `GET /referrals/earnings` - Lifetime referral stats and earnings

</details>


<details open>
<summary>Daily earnings</summary>

- [x] `GET /earnings/stats` - Detailed daily earnings in "normal" mode for the past month
- [x] `GET /jt-earnings/stats` - Detailed daily earnings in JumpTask mode for the past month
- [x] `GET /earnings/wallet-stats` - Daily earnings broken down into normal and JumpTask modes.

</details>


<details open>
<summary>Current day earnings</summary>

- [x] `GET /earnings/today` - Current day earnings for "normal" mode, with detailed information about the origin of your
  earnings.
- [x] `GET /jt-earnings/today` - Current day earnings for JumpTask mode, with detailed information about the origin of
  your earnings.
-

</details>
