from base import *
from botrunner_session import BotRunnerSession

botrunner_supportedmaps = Table('botrunner_supportedmap', Base.metadata,
   Column('botrunner_id', Integer, ForeignKey('botrunner.botrunner_id'),
       nullable=False),
   Column('map_id', Integer, ForeignKey('map.map_id'), nullable=False),
   UniqueConstraint('botrunner_id', 'map_id')
)

botrunner_supportedmods = Table('botrunner_supportedmod', Base.metadata,
   Column('botrunner_id', Integer, ForeignKey('botrunner.botrunner_id'),
       nullable=False),
   Column('mod_id', Integer, ForeignKey('mod.mod_id'), nullable=False),
   UniqueConstraint('botrunner_id', 'mod_id')
)

botrunner_supportedais = Table('botrunner_supportedai', Base.metadata,
   Column('botrunner_id', Integer, ForeignKey('botrunner.botrunner_id'),
       nullable=False),
   Column('ai_id', Integer, ForeignKey('ai.ai_id'), nullable=False),
   UniqueConstraint('botrunner_id', 'ai_id')
)

class BotRunner(Base):
    __tablename__ = 'botrunner'

    botrunner_id = Column(Integer, primary_key=True)
    botrunner_name = Column(String(255), unique=True, nullable=False)
    botrunner_sharedsecret = Column(String(255), nullable=False)
    botrunner_owneraccountid = Column(Integer,
            ForeignKey('account.account_id'))

    owneraccount = relationship("Account")
    supportedmaps = relationship("Map", secondary=botrunner_supportedmaps)
    supportedmods = relationship("Mod", secondary=botrunner_supportedmods)
    supportedais = relationship("AI", secondary=botrunner_supportedais)
    sessions = relationship("BotRunnerSession", uselist=True)

    rowspan = 0

    def __init__(self, botrunner_name, botrunner_sharedsecret):
        self.botrunner_name = botrunner_name
        self.botrunner_sharedsecret = botrunner_sharedsecret
