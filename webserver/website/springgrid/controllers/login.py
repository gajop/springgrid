import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from springgrid.lib.base import BaseController, render

log = logging.getLogger(__name__)

class LoginController(BaseController):
    def login(self):
        """Show login form. Submit to /login/submit"""
        return render('login.html')

    def submit(self):
        """Verify username and password"""
        # Get fields
        form_username = str(request.params.get('username'))
        form_password = str(request.params.get('password'))

        session['user'] = form_username
        session.save()
        return render('loggedin.html')
        # TODO: implement later, just login the user for now
        # Get user from database
        db_user = model.WebUser.query(User).get_by(name=form_user)
        if db_user is None:
            return render('login.html')

        # Wrong password? 
        if db_user.password != bcrypt.hashpw(form_password, db_user.password):
            return render('login.html')

        # Mark user as logged
        session['user'] = form_username
        session.save()

        # Send user back to where they originally wanted
        if session.get('path_before_login'):
            redirect(session['path_before_login'])
        else:
            return render('loggedin.html')

    def logout(self):
        """Log out the user and display a confirmation message"""
        if 'user' in session:
            del session['user']
            session.save()
        return render('logout.html')

