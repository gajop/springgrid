import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from springgrid.lib.base import BaseController, render, Session
from springgrid.model.meta import Mod
from springgrid.model import roles

log = logging.getLogger(__name__)

class ModController(BaseController):
    
    def view(self, id):
        mod = Session.query(Mod).filter(Mod.mod_id == id).first()
        showForm = False
        if roles.isInRole(roles.modadmin):
            showForm = True
            
        c.showForm = showForm
        c.mod = mod
        return render('viewmod.html')

    def list(self):
        mods = Session.query(Mod)
        showForm = False
        if roles.isInRole(roles.modadmin):
            showForm = True
            
        c.showForm = showForm
        c.mods = mods
        return render('viewmods.html')

    def add(self):
        pass
    
    def remove(self, id):
        pass
    
    def update(self, id):
        pass