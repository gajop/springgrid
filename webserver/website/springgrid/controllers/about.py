import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from springgrid.lib.base import BaseController, render

from jinja2 import Environment, PackageLoader

log = logging.getLogger(__name__)

class AboutController(BaseController):

    def index(self):
        return render('about.html')
