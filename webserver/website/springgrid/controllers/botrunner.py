import logging
import datetime
import formencode
from formencode.validators import PlainText, Int, URL, String

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import validate

from springgrid.lib.base import BaseController, render, Session
from springgrid.model import botrunnerhelper, loginhelper, confighelper, roles
from springgrid.model.meta import BotRunner, AIOption
from springgrid.utils import dates

log = logging.getLogger(__name__)


class BotrunnerForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    botrunnerName = String(not_empty=True)
    sharedSecret = PlainText(not_empty=True)


class BotrunnerController(BaseController):

    @validate(schema=BotrunnerForm(), form='list', post_only=True, on_get=False)
    def add(self):
        botrunnerName = self.form_result["botrunnerName"]
        sharedSecret = self.form_result["sharedSecret"]

        botrunner = BotRunner(botrunnerName, sharedSecret)
        Session.add(botrunner)
        Session.commit()

        c.message = "Added ok"
        return render('genericmessage.html')

    def view(self, id):
        botrunner = Session.query(BotRunner).filter(
                BotRunner.botrunner_id == id).first()
        c.isbotrunnerowner = ('user' in session and
                botrunner.owneraccount != None and
                botrunner.owneraccount.username == session['user'])
        c.showform = (c.isbotrunnerowner or
                roles.isInRole(roles.botrunneradmin))

        potentialoptions = [i[0] for i in Session.query(AIOption.option_name)]
        for option in botrunner.options:
            potentialoptions.remove(option.option_name)
        c.botrunner = botrunner
        return render('viewbotrunner.html')

    def list(self):
        #FIXME: this should not be a part of a controller request
        botrunnerhelper.purgeExpiredSessions()
        Session.commit()

        botrunners = Session.query(BotRunner)

# if you know of a reliable way of just adding
#the following two data to  the business ojbects,
# go ahead:
        botrunnerdata = {}
        sessiondata = {}
        for botrunner in botrunners:
            rowspan = 1
            if len(botrunner.sessions) > 1:
                rowspan = len(botrunner.sessions)
            botrunnerdata[botrunner] = {}
            botrunnerdata[botrunner]['rowspan'] = rowspan
            for botSession in botrunner.sessions:
                sessiondata[botSession] = {}
                sessiondata[botSession]['pingtimestatus'] = 'down'
                lastpingtimeddate = None
                lastpingtime = botSession.lastpingtime
                if lastpingtime != None:
                    lastpingtimedate = dates.dateStringToDateTime(lastpingtime)
                    secondssincelastping = dates.timedifftototalseconds(
                            datetime.datetime.now() - lastpingtimedate)
                    sessiondata[botSession]['lastpingtimestring'] =\
                        str(lastpingtimedate)
                    if secondssincelastping < \
                        confighelper.getValue('expiresessionminutes') * 60:
                        sessiondata[botSession]['pingtimestatus'] = 'maybeok'
                    if secondssincelastping < confighelper.getValue(
                            'guimarksessionasmaybedownafterthismanyminutes') \
                            * 60:
                        sessiondata[botSession]['pingtimestatus'] = 'ok'

        c.botrunners = botrunners
        c.isIsLoggedIn = False
        if 'user' in session:
            c.isLoggedIn = True
            c.username = session['user']
        c.botrunnerData = botrunnerdata
        c.sessionData = sessiondata
        return render('viewbotrunners.html')
