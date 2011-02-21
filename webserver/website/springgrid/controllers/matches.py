import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from springgrid.lib.base import BaseController, render, Session
from springgrid.lib.helpers import *
from springgrid.model.meta import MatchRequest

log = logging.getLogger(__name__)

class MatchesController(BaseController):

    def results(self):
        c.requests = Session.query(MatchRequest).filter(MatchRequest.matchresult != None)
        c.requests = paginate.Page(
            c.requests,
            page=1,
            items_per_page=50)
        c.replayPaths = {}
        c.infologPaths = {}
        for request in c.requests:
            replayPath = replaycontroller.getReplayPath(request.matchrequest_id)
            if os.path.isfile(replaypath):
                replayPaths[request] = replaycontroller.getReplayWebRelativePath(request.matchrequest_id)
            if os.path.isfile(replaycontroller.getInfologPath(request.matchrequest_id)):
                infologPaths[request] = replaycontroller.getInfologWebRelativePath(request.matchrequest_id)

        return render('viewresults.html')

    def requests(self):
        c.requests = Session.query(MatchRequest).filter(MatchRequest.matchresult == None)
        c.requests = paginate.Page(
            c.requests,
            page=1,
            items_per_page=50)

        datetimeassignedbyrequest = {}
        for request in c.requests:
            if request.matchrequestinprogress != None:
                datetimeassignedbyrequest[request] = str(dates.dateStringToDateTime(request.matchrequestinprogress.datetimeassigned))

        return render('viewrequests.html')
