import logging
import formencode
from formencode.validators import PlainText, Int, String, StringBool

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import validate

from springgrid.lib.base import BaseController, render, Session
from springgrid.model.meta import League, LeagueAI
from springgrid.model import roles

log = logging.getLogger(__name__)

class LeagueForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    leagueName = String(not_empty=True)
    modId = Int(not_empty=True)
    mapId = Int(not_empty=True)
    speed = Int(not_empty=True)
    softtimeout = Int(not_empty=True)
    hardtimeout = Int(not_empty=True)
    nummatchesperaipair = Int(not_empty=True)
    sides = Int(not_empty=True)
    sidemodes = Int(not_empty=True)
    playagainstself = StringBool(not_empty=True)
#    ais = None
#    if formhelper.getform().has_key('selectedais'):
#        ais = formhelper.getform()['selectedais']
#        ais = [ai.value for ai in ais]

class LeagueController(BaseController):

    @validate(schema=LeagueForm(), form='list', post_only=True, on_get=False)
    def add(self):
        if not roles.isInRole(roles.leagueadmin):
            c.message = "You must be logged in as a leagueadmin"
            return render('genericmessage.html')

        leagueName = self.form_result["leagueName"]
        modId = self.form_result["modId"]
        mapId = self.form_result["mapId"]
        speed = self.form_result["speed"]
        softtimeout = self.form_result["softtimeout"]
        hardtimeout = self.form_result["hardtimeout"]
        nummatchesperaipair = self.form_result["nummatchesperaipair"]
        sides = self.form_result["sides"]
        sidemodes = self.form_result["sidemodes"]
        playagainstself = self.form_result["playagainstself"]

        league = League(leagueName, account, modName, mapName,
                nummatchesperaipair, speed, softtimeout, hardtimeout,
                sides, sidemodes, playagainstself)
        leagueais = [LeagueAI(ai, league) for ai in ais]
        Session.add(league)
        Session.add_all(leagueais)
        Session.commit()

        c.message = "Added ok"
        return render('genericmessage.html')

    def view(self, id):
        league = Session.query(League).filter(League.league_id == id).first()
        if league == None:
            c.message = "No such league"
            return render('genericmessage.html')

        showform = roles.isInRole(roles.leagueadmin)

        c.league = league
        c.showForm = showform
        return render('viewleague.html')

    @validate(schema=LeagueForm(), form='view', post_only=True, on_get=False)
    def update(self, id):
        if not roles.isInRole(roles.leagueadmin):
            c.message = "You must be logged in as a leagueadmin"
            return render('genericmessage.html')

        leagueName = self.form_result['leagueName']
        leagueArchiveChecksum = self.form_result["leagueArchiveChecksum"]
        leagueUrl = self.form_result["leagueUrl"]

        league = Session.query(League).filter(League.league_id == id).first()
        if league == None:
            c.message = "No such league"
            return render('genericmessage.html')

        league.league_name = leagueName
        league.league_url = leagueUrl
        league.league_archivechecksum = leagueArchiveChecksum
        Session.commit()

        c.message = "Updated ok"
        return render('genericmessage.html')

    def remove(self, id):
        if not roles.isInRole(roles.leagueadmin):
            c.message = "You must be logged in as a leagueadmin"
            return render('genericmessage.html')

        league = Session.query(League).filter(League.league_id == id).first()
        if league == None:
            c.message = "No such league"
            return render('genericmessage.html')

        Session.delete(league)
        Session.commit()

        c.message = "Deleted ok"
        return render('genericmessage.html')

    def list(self):
        leagues = Session.query(League)
        showForm = roles.isInRole(roles.leagueadmin)

        c.showForm = showForm
        c.leagues = leagues
        return render('viewleagues.html')
