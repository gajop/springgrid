from base import *
from botrunner_session import BotRunnerSession


class MatchRequestInProgress(Base):
    __tablename__ = 'matchrequests_inprogress'

    matchrequest_id = Column(Integer,
            ForeignKey('matchrequestqueue.matchrequest_id'), primary_key=True)
    botrunner_id = Column(Integer, ForeignKey('botrunner.botrunner_id'),
            nullable=False)
    botrunner_session_id = Column(String(255),
            nullable=False)
    datetimeassigned = Column(DateTime,
            nullable=False)

    __table_args__ = (schema.ForeignKeyConstraint(
        ('botrunner_id', 'botrunner_session_id'),
        ('botrunner_session.botrunner_id',
            'botrunner_session.botrunner_session_id')), {})

    botrunner = relationship("BotRunner")
    botrunnersession = relationship("BotRunnerSession",
            primaryjoin=and_(botrunner_id == BotRunnerSession.botrunner_id,
                botrunner_session_id == BotRunnerSession.botrunner_session_id))

    def __init__(self, botrunner, botrunnersession, datetimeassigned):
        self.botrunner = botrunner
        self.botrunnersession = botrunnersession
        self.datetimeassigned = datetimeassigned
