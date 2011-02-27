import logging
import formencode
from formencode.validators import PlainText, Int, URL, String, StringBool 

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import validate

from springgrid.lib.base import BaseController, render, Session
from springgrid.model.meta import AI, AIOption
from springgrid.model import roles
from springgrid.utils import listhelper

log = logging.getLogger(__name__)

class AIForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    aiName = String(not_empty=True)
    aiVersion = String(not_empty=True)
    needsCompiling = StringBool(if_missing=False)
    downloadUrl = URL(check_exists=True)
    modArchiveChecksum = PlainText(not_empty=True)

class AiController(BaseController):

    @validate(schema=AIForm(), form='list', post_only=True, on_get=False)
    def add(self):
        if not roles.isInRole(roles.aiadmin):
            c.message = "You must be logged in as aiadmin"
            return render('genericmessage.html')

        aiName = self.form_result["aiName"]
        aiVersion = self.form_result["aiVersion"]
        downloadUrl = self.form_result["downloadUrl"]
        needsCompiling = self.form_result["needsCompiling"]

        ai = AI(aiName, aiVersion)
        ai.ai_downloadurl = downloadUrl
        ai.ai_needscompiling = needsCompiling
        ai.owneraccount = accounthelper.getAccount(session['user'])
        Session.add(ai)
        Session.commit()

        c.message = "Added ok"
        return render('genericmessage.html')
    
    def view(self, id):
        ai = Session.query(AI).filter(AI.ai_id == id).first()
        if ai == None:
            c.message = "No such ai"
            return render('genericmessage.html')

        showform = roles.isInRole(roles.aiadmin)
        
        potentialoptions = listhelper.tuplelisttolist(Session.query(AIOption.option_name))
        for option in ai.allowedoptions:
           potentialoptions.remove(option.option_name )
           
        c.ai = ai
        c.showForm = showform
        return render('viewai.html')
    
    @validate(schema=AIForm(), form='view', post_only=True, on_get=False)
    def update(self, id):
        if not roles.isInRole(roles.aiadmin):
            c.message = "You must be logged in as a aiadmin"
            return render('genericmessage.html')

        aiName = self.form_result["aiName"]
        aiVersion = self.form_result["aiVersion"]
        downloadUrl = self.form_result["downloadUrl"]
        needsCompiling = self.form_result["needsCompiling"]
    
        ai = Session.query(AI).filter(AI.ai_id == id).first()
        if ai == None:
            c.message = "No such ai"
            return render('genericmessage.html')

        ai.ai_name = aiName
        ai.ai_version = aiVersion
        ai.ai_downloadurl = downloadUrl
        ai.ai_needscompiling = needsCompiling
        Session.commit()
        
        c.message = "Updated ok"
        return render('genericmessage.html')
    
    def remove(self, id):
        if not roles.isInRole(roles.aiadmin):
            c.message = "You must be logged in as a aiadmin"
            return render('genericmessage.html')
        
        ai = Session.query(AI).filter(AI.ai_id == id).first()
        if ai == None:
            c.message = "No such ai"
            return render('genericmessage.html')

        Session.delete(ai)
        Session.commit()
        
        c.message = "Deleted ok"
        return render('genericmessage.html')

    def list(self):
        ais = Session.query(AI)
        showForm = roles.isInRole(roles.aiadmin)

        c.ais = ais
        c.showForm = showForm
        return render('viewais.html')
