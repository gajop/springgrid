import logging
import os

from pylons import request, response, session, tmpl_context as c, url
from pylons import request
from pylons.controllers.util import abort, redirect

from springgrid.lib.base import BaseController, render, Session
from springgrid.lib.helpers import *
from springgrid.model.meta import MatchRequest
from springgrid.model import replaycontroller
from springgrid.utils import dates

log = logging.getLogger(__name__)

class MatchesController(BaseController):

    def results(self):
        c.requests = Session.query(MatchRequest).filter(MatchRequest.matchresult != None)
        page = 1
        try:
            page = int(request.params['page'])
        except:
            pass
        c.requests = paginate.Page(
            c.requests,
            page=page,
            items_per_page=20)
        c.replayPaths = {}
        c.infologPaths = {}
        for req in c.requests:
            replayPath = replaycontroller.getReplayPath(req.matchrequest_id)
            if os.path.isfile(replayPath):
                c.replayPaths[req] = replaycontroller.getReplayWebRelativePath(req.matchrequest_id)
            if os.path.isfile(replaycontroller.getInfologPath(req.matchrequest_id)):
                c.infologPaths[req] = replaycontroller.getInfologWebRelativePath(req.matchrequest_id)

        return render('viewresults.html')

    def requests(self):
        c.requests = Session.query(MatchRequest).filter(MatchRequest.matchresult == None)
        page = 1
        try:
            page = int(request.params['page'])
        except:
            pass
        c.requests = paginate.Page(
            c.requests,
            page=page,
            items_per_page=20)

        c.datetimeassignedbyrequest = {}
        for req in c.requests:
            if req.matchrequestinprogress != None:
                c.datetimeassignedbyrequest[req] = str(dates.dateStringToDateTime(req.matchrequestinprogress.datetimeassigned))

        return render('viewrequests.html')
