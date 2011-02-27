import logging
import formencode
from formencode.validators import PlainText, Int, URL, String

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import validate

from springgrid.lib.base import BaseController, render, Session
from springgrid.model.meta import Map
from springgrid.model import roles

log = logging.getLogger(__name__)


class MapForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    mapName = String(not_empty=True)
    mapUrl = URL(check_exists=True)
    mapArchiveChecksum = PlainText(not_empty=True)

class MapController(BaseController):
    
    @validate(schema=MapForm(), form='list', post_only=True, on_get=False)
    def add(self):
        if not roles.isInRole(roles.mapadmin):
            c.message = "You must be logged in as a mapadmin"
            return render('genericmessage.html')

        mapname = self.form_result["mapName"]
        maparchivechecksum = self.form_result["mapArchiveChecksum"]
        mapurl = self.form_result["mapUrl"]

        map = Map(mapname)
        map.map_url = mapurl
        map.map_archivechecksum = maparchivechecksum
        Session.add(map)
        Session.commit()

        c.message = "Added ok"
        return render('genericmessage.html')

    def view(self, id):
        map = Session.query(Map).filter(Map.map_id == id).first()
        if map == None:
            c.message = "No such map"
            return render('genericmessage.html')

        showform = roles.isInRole(roles.mapadmin)
           
        c.map = map
        c.showForm = showform
        return render('viewmap.html')
    
    @validate(schema=MapForm(), form='view', post_only=True, on_get=False)
    def update(self, id):
        if not roles.isInRole(roles.mapadmin):
            c.message = "You must be logged in as a mapadmin"
            return render('genericmessage.html')

        mapName = self.form_result['mapName']
        mapArchiveChecksum = self.form_result["mapArchiveChecksum"]
        mapUrl = self.form_result["mapUrl"]
    
        map = Session.query(Map).filter(Map.map_id == id).first()
        if map == None:
            c.message = "No such map"
            return render('genericmessage.html')

        map.map_name = mapName
        map.map_url = mapUrl
        map.map_archivechecksum = mapArchiveChecksum
        Session.commit()
        
        c.message = "Updated ok"
        return render('genericmessage.html')
    
    
    def remove(self, id):
        if not roles.isInRole(roles.mapadmin):
            c.message = "You must be logged in as a mapadmin"
            return render('genericmessage.html')
        
        map = Session.query(Map).filter(Map.map_id == id).first()
        if map == None:
            c.message = "No such map"
            return render('genericmessage.html')

        Session.delete(map)
        Session.commit()
        
        c.message = "Deleted ok"
        return render('genericmessage.html')

    def list(self):
        maps = Session.query(Map)
        showForm = roles.isInRole(roles.mapadmin)
            
        c.showForm = showForm
        c.maps = maps
        return render('viewmaps.html')
    
