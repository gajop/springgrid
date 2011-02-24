import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from springgrid.lib.base import BaseController, render, Session
from springgrid.model.meta import AI, AIOption
from springgrid.model import roles
from springgrid.utils import listhelper

log = logging.getLogger(__name__)

class AiController(BaseController):
    
    def view(self, id):
        ai = Session.query(AI).filter(AI.ai_id == id).first()
        showform = roles.isInRole(roles.aiadmin)
        
        potentialoptions = listhelper.tuplelisttolist(Session.query(AIOption.option_name))
        for option in ai.allowedoptions:
           potentialoptions.remove(option.option_name )
           
        c.ai = ai
        c.showForm = showform
        return render('viewai.html')

    def list(self):
        c.ais = Session.query(AI)
        #c.showform = ( loginhelper.gusername != '' )
        return render('viewais.html')
