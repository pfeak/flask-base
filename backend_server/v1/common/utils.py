from flask import current_app
from flask_jwt_extended.config import config


def set_fresh_cookies(response, encoded_fresh_token, max_age=None):
    """
    :param response: The Flask response object to set the access cookies in.
    :param encoded_fresh_token: The encoded access fresh token to set in the cookies.
    :param max_age: The max age of the cookie. If this is None, it will use the
                    `JWT_SESSION_COOKIE` option (see :ref:`Configuration Options`).
                    Otherwise, it will use this as the cookies `max-age` and the
                    JWT_SESSION_COOKIE option will be ignored.  Values should be
                    the number of seconds (as an integer).
    """
    if not config.jwt_in_cookies:
        raise RuntimeWarning("set_access_cookies() called without "
                             "'JWT_TOKEN_LOCATION' configured to use cookies")

    # Set the access JWT in the cookie
    response.set_cookie(current_app.config['JWT_FRESH_COOKIE_NAME'],
                        value=encoded_fresh_token,
                        max_age=max_age or config.cookie_max_age,
                        secure=config.cookie_secure,
                        httponly=True,
                        domain=config.cookie_domain,
                        path=current_app.config['JWT_FRESH_COOKIE_PATH'],
                        samesite=config.cookie_samesite)
