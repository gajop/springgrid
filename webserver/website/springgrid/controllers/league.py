import logging
import formencode
from formencode.validators import PlainText, Int, String, StringBool
from formencode.compound import All

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import validate

from springgrid.lib.base import BaseController, render, Session
from pylons import url
from pylons.controllers.util import redirect
from springgrid.model.meta import League, LeagueAI, LeagueMap, Mod, ModSide, AI, Map, Account, MatchRequest
from springgrid.model import roles, matchscheduler

log = logging.getLogger(__name__)

class LeagueForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = False
    leagueName = String(not_empty=True)
    modId = Int(not_empty=True)
    speed = Int(not_empty=True)
    softtimeout = Int(not_empty=True)
    hardtimeout = Int(not_empty=True)
    nummatchesperaipair = Int(not_empty=True)
    sides = String(not_empty=True)
    sidemodes = String(not_empty=True)
    playagainstself = StringBool(if_missing=False)

class AIStats:
    def __init__(self, name, version):
        self.name = name
        self.version = version
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.timeouts = 0
        self.crashes = 0
        self.score = 0
        self.games = 0
        self.scheduled = 0

class LeagueController(BaseController):

    @validate(schema=LeagueForm(), form='list', post_only=True, on_get=False)
    def add(self):
        if not roles.isInRole(roles.leagueadmin):
            c.message = "You must be logged in as a leagueadmin"
            return render('genericmessage.html')

        leagueName = self.form_result["leagueName"]
        modId = self.form_result["modId"]
        speed = self.form_result["speed"]
        softtimeout = self.form_result["softtimeout"]
        hardtimeout = self.form_result["hardtimeout"]
        nummatchesperaipair = self.form_result["nummatchesperaipair"]
        sides = self.form_result["sides"]
        sidemodes = self.form_result["sidemodes"]
        playagainstself = self.form_result["playagainstself"]
        account = Session.query(Account).filter(Account.username == session['user']).first()
        ais = []
        for i in range(Session.query(AI).count() + 1):
            ai_i = 'ai_checkbox_' + str(i)
            if (self.form_result.has_key(ai_i)):
                ais.append(i)
        maps = []
        i = 0
        while True:
            map_i = 'mapId' + str(i)
            if not self.form_result.has_key(map_i):
                break
            maps.append(self.form_result[map_i])
            i = i + 1
        print(maps)
        league = League(leagueName, account, modId,
                nummatchesperaipair, speed, softtimeout, hardtimeout,
                sides, sidemodes, playagainstself)
        leagueAIs = [LeagueAI(ai, league) for ai in ais]
        leagueMaps = [LeagueMap(map, league) for map in maps]
        Session.add(league)
        Session.add_all(leagueAIs)
        Session.add_all(leagueMaps)

        matchrequests = Session.query(MatchRequest).filter(MatchRequest.league_id ==\
                league.league_id)
        matchresults = [req for req in matchrequests if req.matchresult != None] 

        matchscheduler.addLeagueMatches(league, matchrequests, matchresults)
        Session.flush()
        Session.commit()

        redirect(url(controller='league', action='view', id=league.league_id))

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
        
        Session.query(LeagueAI).filter(LeagueAI.league_id == id).delete()
        Session.delete(league)
        Session.commit()

        c.message = "Deleted ok"
        return render('genericmessage.html')

    def list(self):
        leagues = Session.query(League)
        showForm = roles.isInRole(roles.leagueadmin)
        mods = Session.query(Mod)
        ais = Session.query(AI)
        tmpais = {}
        maps = Session.query(Map)
        c.maps = {}
        for map in maps:
            c.maps[map.map_id] = map.map_name
        mods = Session.query(Mod)
        c.mods = {}
        for mod in mods:
            c.mods[mod.mod_id] = mod.mod_name

        modsides = {}
        for i, mod in enumerate(mods):
            sides = Session.query(ModSide).filter(ModSide.mod_id == mod.mod_id)
            modsides[mod.mod_name] = (i, [])
            for side in sides:
                modsides[mod.mod_name][1].append((side.mod_side_name, side.mod_side_id))

        for ai in ais:
            tmpais[ai.ai_id] = ai.ai_base.ai_base_name + " " + ai.ai_version

        c.ais = tmpais
        c.sides = modsides
        c.showForm = showForm
        c.leagues = leagues
        c.sidemodes = { "allsame" : "All same", "xvsy" : "X vs Y" }
        c.speeds = [20] #default
        c.speeds.extend(range(1, 10))
        c.speeds.extend(range(10, 101, 5))
        c.timeouts = c.speeds
        return render('viewleagues.html')

    def view(self, id):
        #check if any leagues exist
        if len(Session.query(League).all()) == 0:
            c.message = "Please create a league first."            
            return render('genericmessage.html')
       
        #get the league by id, or choose the first one
        league = Session.query(League).filter(League.league_id == id).first()

        #get map name
        c.map_names = Session.query(Map).join(LeagueMap).filter(LeagueMap.league_id == league.league_id).values('map_name')
        c.mod_name = Session.query(Mod).filter(Mod.mod_id == league.mod_id).first().mod_name

        #get the league ais that are part of the chosen league
        ais = Session.query(AI).join(LeagueAI).filter(LeagueAI.league_id ==\
                league.league_id)

        #get matches that have been played in the league so far 
        matchRequests = Session.query(MatchRequest).filter(MatchRequest.league_id ==\
                league.league_id) 

        aistats = {}
        for ai in ais:
            aistats[(ai.ai_base.ai_base_name, ai.ai_version)] = AIStats(ai.ai_base.ai_base_name, ai.ai_version)

        for match in matchRequests:
            first = True
            for ai in [match.ai0, match.ai1]:
                aistat = aistats[ai.ai_base.ai_base_name, ai.ai_version]
                aistat.games += 1
                matchresult = match.matchresult
                if matchresult is None:
                    aistat.scheduled += 1
                else:
                    if matchresult.matchresult == 'draw':
                        aistat.draws += 1
                        aistat.score += 1
                    elif matchresult.matchresult == 'crashed':
                        aistat.crashes += 1
                        aistat.score += 1
                    elif matchresult.matchresult == 'gametimeout':
                        aistat.timeouts += 1
                        aistat.score += 1
                    elif matchresult.matchresult == 'ai0won':
                        if first:
                            aistat.wins += 1
                            aistat.score += 3
                        else:
                            aistat.losses += 1
                    elif matchresult.matchresult == 'ai1won':
                        if first:
                            aistat.losses += 1
                        else:
                            aistat.wins += 1
                            aistat.score += 3
                first = False
        aistats = sorted(aistats.itervalues(), key=lambda x: -x.score)
        
        c.aistats = aistats
        c.league = league
        c.leagues = Session.query(League).all()
        return render('viewleague.html') 
        

