import logging
import formencode
from formencode.validators import PlainText, Int, URL

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import validate

from springgrid.lib.base import BaseController, render, Session
from springgrid.model.meta import Map
from springgrid.model import roles

log = logging.getLogger(__name__)


class MapUpdateForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    mapName = PlainText(not_empty=True)
    mapArchiveChecksum = PlainText(not_empty=True)
    mapUrl = URL(check_exists=True)

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
        if roles.isInRole(roles.mapadmin):
            showForm = True
            
        c.showForm = showForm
        c.maps = maps
        return render('viewmaps.html')
    
    @validate(schema=MapUpdateForm(), form='view', post_only=True, on_get=False)
    def update(self, id):
        if not roles.isInRole(roles.mapadmin):
            return "You must be logged in as a mapadmin"
        else:
            mapName = self.form_result['mapName']
            mapArchiveChecksum = self.form_result["mapArchiveChecksum"]
            mapUrl = self.form_result["mapUrl"]
        
            map = Session.query(Map).filter(Map.map_id == id).first()
            map.map_name = mapName
            map.map_url = mapUrl
            map.map_archivechecksum = mapArchiveChecksum
            Session.commit()
            return "Updated ok"
    
    def remove(self, id):
        pass