# coding: utf-8
import mechanize
import cookielib


class BaseBroker(object):
    portifolio = None
    cookies = dict()

    def authenticate(self, user, password):
        """
        Returns
        --------
        Return
        """
        raise NotImplementedError

    def sell(self, symbol, shares, price):
        """
        Returns
        --------
        Return
        """
        raise NotImplementedError

    def buy(self, symbol, shares, price):
        """
        Returns
        --------
        Return
        """
        raise NotImplementedError


def login_check(method):
    """Checker decorator"""

    def wrapper(self, *args, **kwargs):
        if self.browser:
            return method(self, *args, **kwargs)
        else:
            raise Exception("Not logged!")

    return wrapper
