import logging
import os

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from springgrid.lib.base import BaseController, render
from springgrid.utils import filehelper
from springgrid.model import confighelper

log = logging.getLogger(__name__)

class InfoController(BaseController):

    def botrunner(self):
        return render('startbotrunner.html')

    def setupnotes(self):
        x = open("howtouse.txt")
        text = x.read()
        return "<pre>" + text + "</pre>"

    def config(self):
        c.config = confighelper.getconfigdict()
        return render('viewconfig.html')

    def diagnostics(self):
        # check replays directory is writable
        c.canWrite = False
        c.dirExists = True
        if not os.path.exists("replays"):
            try:
                os.makedirs("replays" )
            except:
                c.dirExists = False

        if c.dirExists:
            #testfilepath = scriptdir + "/replays/~test"
            if os.access('replays/', os.W_OK):
                c.canWrite = True
                print os.access('replays/', os.W_OK)
        return render('diagnostics.html')
