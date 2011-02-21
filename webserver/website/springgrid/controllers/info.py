import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from springgrid.lib.base import BaseController, render
from springgrid.utils import filehelper

log = logging.getLogger(__name__)

class InfoController(BaseController):

    def botrunner(self):
        return render('startbotrunner.html')

    def setupnotes(self):
        return "<pre>" + filehelper.readFile("howtouse.txt") + "</pre>"
