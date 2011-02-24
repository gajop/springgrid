import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from springgrid.lib.base import BaseController, render, Session
from springgrid.model.meta import Map
from springgrid.model import roles

log = logging.getLogger(__name__)

class MapController(BaseController):
    
    def view(self, id):
        map = Session.query(Map).filter(Map.map_id == id).first()
        showform = False
        if roles.isInRole(roles.mapadmin):
           showform = True
           
        c.map = map
        c.showForm = showform
        return render('viewmap.html')

    def list(self):
        maps = Session.query(Map)
        showForm = False
        #if roles.isInRole(roles.mapadmin):
        #    showForm = True
            
        c.showForm = showForm
        c.maps = maps
        return render('viewmaps.html')