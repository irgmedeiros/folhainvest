# coding: utf-8


class BaseTrader(object):
    portifolio = None
    broker = None

    @property
    def portifolio(self):
        """
        Returns
        --------
        Return
        """
        return self.portifolio

    @property
    def broker(self):
        """
        Returns
        --------
        Return
        """
        return self.broker

    def authenticate(self, user, password):
        self.broker.authenticate(user, password)



