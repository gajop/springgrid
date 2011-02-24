import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import validate

from springgrid.model.meta import Account
from springgrid.model import loginhelper

from springgrid.lib.base import BaseController, render
import formencode

log = logging.getLogger(__name__)

class LoginForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    username = formencode.validators.PlainText(not_empty=True)
    password = formencode.validators.PlainText(not_empty=True)
    
class OpenIDForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    openidurl = formencode.validators.PlainText(not_empty=True)

class LoginController(BaseController):
    def form(self):
        """Show login form. """
        return render('login.html')

    @validate(schema=LoginForm(), form='form', post_only=True, on_get=False)
    def submit(self):
        """Verify username and password"""        
        password = self.form_result['password']
        username = self.form_result['username']
        
        if not loginhelper.validateUsernamePassword(username, password):
            return render('login.html')

        # Mark user as logged
        session['user'] = username
        session.save()

        # Send user back to where they originally wanted
        if session.get('path_before_login'):
            redirect(session['path_before_login'])
        else:
            return render('loggedin.html')
    
    @validate(schema=OpenIDForm(), form='form', post_only=True, on_get=False)
    def openid(self):
        """Verify openid account"""
        openidurl = self.form_result['openidurl']

    def logout(self):
        """Log out the user and display a confirmation message"""
        if 'user' in session:
            del session['user']
            session.save()
        return render('logout.html')

