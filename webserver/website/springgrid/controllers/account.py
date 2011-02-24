import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from springgrid.lib.base import BaseController, render, Session
from springgrid.model.meta import Account

log = logging.getLogger(__name__)

class AccountController(BaseController):

    def list(self):
        #if loginhelper.gusername == '':
        #    jinjahelper.message( "Please login first before using this page." )
        #    return

        c.accounts = Session.query(Account)

        #showform = roles.isInRole(roles.accountadmin)
        return render('viewaccounts.html')
