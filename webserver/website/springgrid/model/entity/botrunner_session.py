from base import *


class BotRunnerSession(Base):
    __tablename__ = 'botrunner_session'

    botrunner_id = Column(Integer, ForeignKey('botrunner.botrunner_id'),
            primary_key=True)
    botrunner_session_id = Column(String(255), primary_key=True)
    lastpingstatus = Column(String(255), nullable=False)
    lastpingtime = Column(DateTime, nullable=False)
    downloadingai_id = Column(Integer, ForeignKey('ai.ai_id'),
            nullable=True)

    # keep track of any ai being downloaded by this session
    downloadingai = relationship("AI")

    def __init__(self, botrunner_session_id):
        self.botrunner_session_id = botrunner_session_id

        self.pingtimeok = False  # used by viewbotrunners.py
        self.lastpingtimestring = ''  # used by viewbotrunners.py
