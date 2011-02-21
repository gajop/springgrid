import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from springgrid.lib.base import BaseController, render, Session
from springgrid.model.meta import AI, Map, Mod, ModSide, AIOption
from springgrid.utils import *

log = logging.getLogger(__name__)

class SubmitRequestController(BaseController):

    def form(self):
        c.ais = Session.query(AI.ai_name, AI.ai_version)
        c.maps = listhelper.tuplelisttolist(Session.query(Map.map_name))
        c.mods = Session.query(Mod)
        sidequery = Session.query(ModSide)
        c.sides = {}
        for i, mod in enumerate(c.mods):
            c.sides[mod.mod_id] = (i, [])
        for side in sidequery:
            c.sides[side.mod_id][1].append((side.mod_side_name, side.mod_side_id))
            c.mods = [mod.mod_name for mod in c.mods]

        c.options = listhelper.tuplelisttolist(Session.query(AIOption.option_name))

        c.aiitems = []
        c.aivalues = []
        for ai in c.ais:
            aivalues.append(ai.ai_name + " " + ai.ai_version)
            aiitems.append(ai.ai_name + "|" + ai.ai_version)
        c.speeds = [i for i in range(1, 10)]
        c.speeds.extend([i for i in range(10,101,5)])
        c.timeouts = c.speeds
        return render('submitrequestform.html')

    def submit(self):
        pass
