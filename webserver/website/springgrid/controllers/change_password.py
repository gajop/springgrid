import logging
import formencode
from formencode.validators import PlainText, FieldsMatch

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import validate

from springgrid.lib.base import BaseController, render
from springgrid.model import loginhelper

log = logging.getLogger(__name__)


class ChangePasswordForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    oldPassword = PlainText(not_empty=True)
    password = PlainText(not_empty=True)
    confirmPassword = PlainText(not_empty=True)
    chained_validators = [FieldsMatch('password', 'confirmPassword')]

class ChangePasswordController(BaseController):

    def form(self):
        """Show the ChangePassword form."""
        return render('changepasswordform.html')

    @validate(schema=ChangePasswordForm(), form='form', post_only=True, on_get=False)
    def submit(self):
        if 'user' not in session:
            c.message = "Please log in first."
            return render('genericmessage.html')

        oldPassword = self.form_result['oldPassword']
        password = self.form_result['password']
        confirmPassword = self.form_result['confirmPassword']

        # check oldpassword
        if not loginhelper.validateUsernamePassword(
                session['user'], oldPassword):
            c.message = "Please check your old password and try again"
            return render('genericmessage.html')

        if loginhelper.changePassword(session['user'], password):
            c.message = "Password changed ok"
            return render('genericmessage.html')
        else:
            c.message = "Something went wrong. " +\
                    "Please check your values and try again."
            return render('genericmessage.html')
