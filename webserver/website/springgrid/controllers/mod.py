import logging
import formencode
from formencode.validators import PlainText, Int, URL, String

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import validate

from springgrid.lib.base import BaseController, render, Session
from springgrid.model.meta import Mod
from springgrid.model import roles

log = logging.getLogger(__name__)

class ModForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    modName = String(not_empty=True)
    modUrl = URL(check_exists=True)
    modArchiveChecksum = PlainText(not_empty=True)

class ModController(BaseController):

    @validate(schema=ModForm(), form='list', post_only=True, on_get=False)
    def add(self):
        if not roles.isInRole(roles.modadmin):
            c.message = "You must be logged in as a modadmin"
            return render('genericmessage.html')
            
        modname = self.form_result["modName"]
        modarchivechecksum = self.form_result["modArchiveChecksum"]
        modurl = self.form_result["modUrl"]

        mod = Mod(modname)
        mod.mod_url = modurl
        mod.mod_archivechecksum = modarchivechecksum
        Session.add(mod)
        Session.commit()

        c.message = "Added ok"
        return render('genericmessage.html')
    
    def view(self, id):
        mod = Session.query(Mod).filter(Mod.mod_id == id).first()
        if mod == None:
            c.message = "No such mod"
            return render('genericmessage.html')

        showForm = roles.isInRole(roles.modadmin)
            
        c.showForm = showForm
        c.mod = mod
        return render('viewmod.html')
    
    @validate(schema=ModForm(), form='view', post_only=True, on_get=False)
    def update(self, id):
        if not roles.isInRole(roles.modadmin):
            c.message = "You must be logged in as a modadmin"
            return render('genericmessage.html')
        
        modName = self.form_result['modName']
        modArchiveChecksum = self.form_result["modArchiveChecksum"]
        modUrl = self.form_result["modUrl"]
    
        mod = Session.query(Mod).filter(Mod.mod_id == id).first()
        if mod == None:
            c.message = "No such mod"
            return render('genericmessage.html')

        mod.mod_name = modName
        mod.mod_url = modUrl
        mod.mod_archivechecksum = modArchiveChecksum
        Session.commit()
        
        c.message = "Updated ok"
        return render('genericmessage.html')
    
    def remove(self, id):
        if not roles.isInRole(roles.modadmin):
            c.message = "You must be logged in as a modadmin"
            return render('genericmessage.html')
        
        mod = Session.query(Mod).filter(Mod.mod_id == id).first()
        if mod == None:
            c.message = "No such mod"
            return render('genericmessage.html')

        Session.delete(mod)
        Session.commit()
        
        c.message = "Deleted ok"
        return render('genericmessage.html')

    def list(self):
        mods = Session.query(Mod)
        showForm = roles.isInRole(roles.modadmin):
            
        c.showForm = showForm
        c.mods = mods
        return render('viewmods.html')
    
    
