import logging
import formencode
from formencode.validators import PlainText, Int, URL, String, Email

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import validate

from springgrid.lib.base import BaseController, render, Session
from springgrid.model.meta import Account, Role, PasswordInfo
from springgrid.model import roles

log = logging.getLogger(__name__)


class AccountForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    username = PlainText(not_empty=True)
    userfullname = String()
    email = Email(not_empty=True)
    password = PlainText(not_empty=True)


class AccountController(BaseController):

    @validate(schema=AccountForm(), form='list', post_only=True, on_get=False)
    def add(self):
        if not roles.isInRole(roles.accountadmin):
            c.message = "You must be logged in as a accountadmin"
            return render('genericmessage.html')

        username = self.form_result['username']
        userfullname = self.form_result['userfullname']
        email = self.form_result['email']
        password = self.form_result['password']

        account = Account(username, userfullname)
        account.passwordinfo = PasswordInfo(password)
        account.email = email
        Session.add(account)
        Session.commit()

        c.message = "Added ok"
        return render('genericmessage.html')

    def view(self, id):
        account = Session.query(Account).filter(
                Account.account_id == id).first()

        showform = roles.isInRole(roles.accountadmin)

        potentialroles = [i[0] for i in Session.query(Role.role_name)]
        for role in account.roles:
            potentialroles.remove(role.role_name)

        c.account = account
        c.showForm = showform
        return render('viewaccount.html')

    @validate(schema=AccountForm(), form='view', post_only=True, on_get=False)
    def update(self, id):
        if not roles.isInRole(roles.accountadmin):
            c.message = "You must be logged in as a accountadmin"
            return render('genericmessage.html')

        accountName = self.form_result['accountName']
        accountArchiveChecksum = self.form_result["accountArchiveChecksum"]
        accountUrl = self.form_result["accountUrl"]

        account = Session.query(Account).filter(
                Account.account_id == id).first()
        if account == None:
            c.message = "No such account"
            return render('genericmessage.html')

        account.account_name = accountName
        account.account_url = accountUrl
        account.account_archivechecksum = accountArchiveChecksum
        Session.commit()

        c.message = "Updated ok"
        return render('genericmessage.html')

    def remove(self, id):
        if not roles.isInRole(roles.accountadmin):
            c.message = "You must be logged in as a accountadmin"
            return render('genericmessage.html')

        account = Session.query(Account).filter(
                Account.account_id == id).first()
        if account == None:
            c.message = "No such account"
            return render('genericmessage.html')

        if roles.isInRole2(account.username, roles.accountadmin):
            c.message = "Please drop the accountadmin role from "
            return render('genericmessage.html')

        if account.passwordinfo != None:
            Session.delete(account.passwordinfo)
        for openid in account.openids:
            Session.delete(openid)
        Session.delete(account)
        Session.commit()

        c.message = "Deleted ok"
        return render('genericmessage.html')

    def list(self):
        #if loginhelper.gusername == '':
        #    jinjahelper.message( "Please login first before using this page.")
        #    return

        c.accounts = Session.query(Account)
        c.roles = roles

        showform = roles.isInRole(roles.accountadmin)
        return render('viewaccounts.html')
