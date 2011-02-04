"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons import tmpl_context as c, url
from pylons.controllers import WSGIController
from pylons.templating import render_jinja2

from springgrid.model.meta import Session
from springgrid.lib.menu import *

class BaseController(WSGIController):
    requires_auth = False

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            Session.remove()

    def __before__(self):
        if self.requires_auth and 'user' not in session:
            session['path_before_login'] = request.path_info
            session.save()
            redirect(url(controller='login'))

def render(url):
    c.menus = getMenus()
    return render_jinja2(url)
