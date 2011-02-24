from base import *

class BotRunnerSession(Base):
   __tablename__ = 'botrunner_sessions'

   botrunner_id = Column(Integer,ForeignKey('botrunners.botrunner_id'), primary_key = True )
   botrunner_session_id = Column(String(255), primary_key = True)
   lastpingstatus = Column(String(255), nullable = False)
   lastpingtime = Column(String(255), nullable = False)
   downloadingai_id = Column(Integer,ForeignKey('ais.ai_id'), nullable = True)

   downloadingai = relation("AI")  # keep track of any ai being downloaded by this session

   def __init__(self, botrunner_session_id ):
      self.botrunner_session_id = botrunner_session_id

      self.pingtimeok = False # used by viewbotrunners.py
      self.lastpingtimestring = '' # used by viewbotrunners.py