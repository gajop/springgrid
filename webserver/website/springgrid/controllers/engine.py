import logging
import formencode
from formencode.validators import PlainText, Int, URL, String

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import validate

from springgrid.lib.base import BaseController, render, Session
from springgrid.model.meta import Engine
from springgrid.model import roles

log = logging.getLogger(__name__)


class EngineForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    engineName = String(not_empty=True)
    engineUrl = URL(check_exists=True)
    engineArchiveChecksum = PlainText(not_empty=True)


class EngineController(BaseController):

    @validate(schema=EngineForm(), form='list', post_only=True, on_get=False)
    def add(self):
        if not roles.isInRole(roles.modadmin):
            c.message = "You must be logged in as a modadmin. Sorry, temporary"
            return render('genericmessage.html')

        enginename = self.form_result["engineName"]
        enginearchivechecksum = self.form_result["engineArchiveChecksum"]
        engineurl = self.form_result["engineUrl"]

        engine = Engine(enginename)
        engine.engine_url = engineurl
        engine.engine_archivechecksum = enginearchivechecksum
        Session.add(engine)
        Session.commit()

        c.message = "Added ok"
        return render('genericmessage.html')

    def view(self, id):
        engine = Session.query(Engine).filter(Engine.engine_id == id).first()
        if engine == None:
            c.message = "No such engine"
            return render('genericmessage.html')

        showForm = roles.isInRole(roles.modadmin)

        c.showForm = showForm
        c.engine = engine
        return render('viewengine.html')

    @validate(schema=EngineForm(), form='view', post_only=True, on_get=False)
    def update(self, id):
        if not roles.isInRole(roles.modadmin):
            c.message = "You must be logged in as a modadmin"
            return render('genericmessage.html')

        engineName = self.form_result['engineName']
        engineArchiveChecksum = self.form_result["engineArchiveChecksum"]
        engineUrl = self.form_result["engineUrl"]

        engine = Session.query(Engine).filter(Engine.engine_id == id).first()
        if engine == None:
            c.message = "No such engine"
            return render('genericmessage.html')

        engine.engine_name = engineName
        engine.engine_url = engineUrl
        engine.engine_archivechecksum = engineArchiveChecksum
        Session.commit()

        c.message = "Updated ok"
        return render('genericmessage.html')

    def remove(self, id):
        if not roles.isInRole(roles.modadmin):
            c.message = "You must be logged in as a modadmin, temporary!"
            return render('genericmessage.html')

        engine = Session.query(Engine).filter(Engine.engine_id == id).first()
        if engine == None:
            c.message = "No such engine"
            return render('genericmessage.html')

        Session.delete(engine)
        Session.commit()

        c.message = "Deleted ok"
        return render('genericmessage.html')

    def list(self):
        engines = Session.query(Engine)
        showForm = roles.isInRole(roles.modadmin)

        c.showForm = showForm
        c.engines = engines
        return render('viewengines.html')
