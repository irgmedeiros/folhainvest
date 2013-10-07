# coding: utf-8
import locale

from base import BaseBroker, login_check
import mechanize
import cookielib


class FolhaBroker(object):
    def __init__(self):
        self.browser = None
        locale.setlocale(locale.LC_ALL, ('pt_BR', 'UTF-8')) #TODO move to the right place

    @login_check
    def buy(self, symbol, shares, price):
        url = str.format('http://folhainvest.folha.com.br/comprar')
        br = self.browser
        br.open(url)
        br.select_form(nr=0)
        if price:
            #transation with fixed price
            br.form['pricing'] = ['fixed']
            br.form['value'] = locale.format("%.2f", price)
        else:
            #transation with market price
            br.form['pricing'] = ['market']
        br.form['company'] = [str(symbol)]  #TODO: check if symbol is valid to avoid exception here
        br.form['quantity'] = str(shares)
        br.submit()

        req = mechanize.Request('http://folhainvest.folha.com.br/confirmar', r'confirm.x=52&confirm.y=15')
        br.open(req)

        if 'Ordem cancelada' in br.response().read():
            # TODO: show error message
            print('Ordem cancelada')

    @login_check
    def sell(self, symbol, shares, price=None):
        url = str.format('http://folhainvest.folha.com.br/vender')
        br = self.browser
        br.open(url)
        br.select_form(nr=0)
        if price:
            #transation with fixed price
            br.form['pricing'] = ['fixed']
            br.form['value'] = locale.format("%.2f", price)
        else:
            #transation with market price
            br.form['pricing'] = ['market']
        br.form['company'] = [str(symbol)]  #TODO: check if symbol is valid to avoid exception here
        br.form['quantity'] = str(shares)
        br.submit()

        req = mechanize.Request('http://folhainvest.folha.com.br/confirmar', r'confirm.x=34&confirm.y=9')
        br.open(req)

        if 'Ordem cancelada' in br.response().read():
            # TODO: show error message
            print('Ordem cancelada')

    def authenticate(self, user, password):
        br = mechanize.Browser()

        # Cookie Jar
        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)

        # Browser options
        br.set_handle_equiv(True)
        br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)

        # Follows refresh 0 but not hangs on refresh > 0
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        # Want debugging messages?
        br.set_debug_http(True)
        br.set_debug_redirects(True)
        br.set_debug_responses(True)

        # User-Agent (this is cheating, ok?)
        br.addheaders = [('User-agent',
                          'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

        br.open('http://login.folha.com.br/login?done=http%3A%2F%2Ffolhainvest.folha.com.br%2Fcarteira&service=folhainvest')

        br.select_form(nr=0)
        br.form[r'email'] = user
        br.form[r'password'] = password

        br.submit()
        self.browser = br
        if 'Log Out' in br.response().read():
            self.browser = br
        else:
            raise Exception("Couldn't login")


