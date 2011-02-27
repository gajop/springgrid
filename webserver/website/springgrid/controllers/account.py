import logging
import formencode
from formencode import PlainText

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from springgrid.lib.base import BaseController, render, Session
from springgrid.model.meta import Account, Role
from springgrid.model import roles
from springgrid.utils import listhelper

log = logging.getLogger(__name__)

class AccountController(BaseController):

    def list(self):
        #if loginhelper.gusername == '':
        #    jinjahelper.message( "Please login first before using this page." )
        #    return

        c.accounts = Session.query(Account)
        c.roles = roles

        showform = roles.isInRole(roles.accountadmin)
        return render('viewaccounts.html')

    def view(self, id):
        account = Session.query(Account).filter(Account.account_id == id).first()

        showform = roles.isInRole(roles.accountadmin)

        potentialroles = listhelper.tuplelisttolist(Session.query(Role.role_name) )
        for role in account.roles:
            potentialroles.remove(role.role_name)

        c.account = account
        c.showForm = showform
        return render('viewaccount.html')
