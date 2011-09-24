import logging
import os

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from springgrid.lib.base import BaseController, render
from springgrid.model import confighelper

log = logging.getLogger(__name__)


class InfoController(BaseController):

    def botrunner(self):
        return render('startbotrunner.html')

    def config(self):
        c.config = confighelper.getconfigdict()
        return render('viewconfig.html')

    def diagnostics(self):
        # check replays directory is writable
        canWrite = False
        dirExists = True
        if not os.path.exists("replays"):
            try:
                os.makedirs("replays")
            except:
                dirExists = False

        if dirExists:
            if os.access('replays/', os.W_OK):
                canWrite = True

        c.canWrite = canWrite
        c.dirExists = dirExists
        return render('diagnostics.html')
