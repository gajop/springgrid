import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from springgrid.lib.base import BaseController, render, Session
from springgrid.model.meta import Map

log = logging.getLogger(__name__)

class MapController(BaseController):

    def list(self):
        maps = Session.query(Map)
        showForm = False
        #if roles.isInRole(roles.mapadmin):
        #    showForm = True
            
        c.showForm = showForm
        c.maps = maps
        return render('viewmaps.html')