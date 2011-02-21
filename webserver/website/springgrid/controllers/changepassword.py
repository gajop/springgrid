import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from springgrid.lib.base import BaseController, render

log = logging.getLogger(__name__)

class ChangePasswordController(BaseController):
    def form(self):
        """Show the ChangePassword form."""
        pass

    def submit(self):
        return render('changepasswordform.html')
