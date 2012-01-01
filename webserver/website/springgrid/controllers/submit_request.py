import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import validate

from springgrid.lib.base import BaseController, render, Session
from springgrid.model.meta import AI, AIBase, Map, Mod, ModSide, MatchRequest
from springgrid.utils import *
import formencode
from formencode.validators import Int, String

log = logging.getLogger(__name__)

class SubmitRequestForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    ai0 = Int(not_empty=True)
    ai0side = Int(not_empty=True)
    ai1 = Int(not_empty=True)
    ai1side = Int(not_empty=True)
    mapname = String(not_empty=True)
    modname = String(not_empty=True)
    speed = Int(not_empty=True)
    softtimeout = Int(not_empty=True)
    hardtimeout = Int(not_empty=True)

class SubmitRequestController(BaseController):

    def form(self):
        c.ais = Session.query(AIBase)
        c.maps = [i[0] for i in Session.query(Map.map_name)]
        c.mods = Session.query(Mod)
        sidequery = Session.query(ModSide)
        c.sides = {}
        for i, mod in enumerate(c.mods):
            c.sides[mod.mod_id] = (i, [])
        for side in sidequery:
            c.sides[side.mod_id][1].append((side.mod_side_name, side.mod_side_id))

        c.mods = [mod.mod_name for mod in c.mods]
        c.aiitems = []
        c.aivalues = []
        for ai in c.ais:
            for ai_version in ai.versions:
                c.aivalues.append(ai.ai_base_name + " " + ai_version.ai_version)
                c.aiitems.append(ai_version.ai_id)
        c.speeds = [i for i in range(1, 10)]
        c.speeds.extend([i for i in range(10,101,5)])
        c.timeouts = c.speeds
        return render('submitrequestform.html')

    @validate(schema=SubmitRequestForm(), form='form', post_only=True, on_get=False)
    def submit(self):
        map = Session.query(Map).filter(Map.map_name == self.form_result['mapname']).first()
        mod = Session.query(Mod).filter(Mod.mod_name == self.form_result['modname']).first()
        ai0 = Session.query(AI).filter(AI.ai_id == self.form_result['ai0']).first()
        ai1 = Session.query(AI).filter(AI.ai_id == self.form_result['ai1']).first()
        ai0side = Session.query(ModSide).filter(ModSide.mod_side_id == self.form_result['ai0side']).first()
        ai1side = Session.query(ModSide).filter(ModSide.mod_side_id == self.form_result['ai1side']).first()

        matchrequest = MatchRequest(ai0 = ai0, ai1 = ai1, map = map, mod = mod,
                                    speed = self.form_result['speed'],
                                    softtimeout = self.form_result['softtimeout'],
                                    hardtimeout = self.form_result['hardtimeout'],
                                    ai0_side=ai0side, ai1_side=ai1side)

        Session.add(matchrequest)

        Session.commit()

        return "Submitted ok."
