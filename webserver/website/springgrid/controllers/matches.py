import logging
import os
import webob
import re

from webob import Response 

from pylons import request, response, session, tmpl_context as c, url
from pylons import request
from pylons.controllers.util import abort, redirect

from springgrid.lib.base import BaseController, render, Session
from springgrid.lib.helpers import *
from springgrid.model.meta import MatchRequest
from springgrid.model import roles, replaycontroller

log = logging.getLogger(__name__)
scriptdir = os.path.dirname(os.path.realpath( __file__ ))

class MatchesController(BaseController):

    def results(self):
        c.requests = Session.query(MatchRequest).filter(
                MatchRequest.matchresult != None)

        try:
            league_id = int(request.params['league'])
            c.requests = c.requests.filter(MatchRequest.league_id == league_id)
        except:
            pass

        page = 1
        try:
            page = int(request.params['page'])
        except:
            pass
        c.requests = paginate.Page(
            c.requests,
            page=page,
            items_per_page=20)
        c.page = page

        c.spoil = 1
        try:
            c.spoil = int(request.params['spoil'])
        except:
            pass

        c.replayPaths = {}
        c.infologPaths = {}

        c.pager = c.requests.pager('Page $page: $link_previous $link_next ~4~')
        params = "&spoil=" + str(c.spoil)
        if request.params.has_key('league'):
            params = params + "&league=" + request.params['league']
        c.pager = re.sub(r"\?page=(\d+)", r"?page=\1" + params, c.pager)
        for req in c.requests:
            replayPath = replaycontroller.getReplayPath(req.matchrequest_id)
            if os.path.isfile(replayPath):
                c.replayPaths[req] = replaycontroller.getReplayWebRelativePath(
                        req.matchrequest_id)
            if os.path.isfile(
                    replaycontroller.getInfologPath(req.matchrequest_id)):
                c.infologPaths[req] = replaycontroller.\
                        getInfologWebRelativePath(req.matchrequest_id)

        return render('viewresults.html')

    def requests(self):
        c.requests = Session.query(MatchRequest).filter(
                MatchRequest.matchresult == None)

        try:
            league_id = int(request.params['league'])
            c.requests = c.requests.filter(MatchRequest.league_id == league_id)
        except:
            pass

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
                c.datetimeassignedbyrequest[req] = \
                        req.matchrequestinprogress.datetimeassigned

        return render('viewrequests.html')
        
    def replays(self, id):
        try:
            downloadFile = open(scriptdir + "/../replays/" + id, 'r').read()
            # application/octet-stream is a fairly generic way of saying that the file should be saved on the disk
            response.content_type = "application/octet-stream"
            # NOTICE: We aren't using compressed files anymore so this probably isn't needed
            #response.content_type = 'application/x-bzip-compressed-tar'
            return downloadFile
        except IOError:
            raise  
            
    def remove(self, id):
        if not roles.isInRole(roles.leagueadmin):
            c.message = "You must be logged in as a leagueadmin"
            return render('genericmessage.html')
        
        request = Session.query(MatchRequest).filter(MatchRequest.matchrequest_id == id).first()
        
        if request == None:
            c.message = "No such request"
            return render('genericmessage.html')   
        
        Session.delete(request)
        Session.commit()
        
        c.message = "Deleted ok"
        return render('genericmessage.html')    
       
