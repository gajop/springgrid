from base import *
from botrunner_session import BotRunnerSession

botrunner_supportedmaps = Table( 'botrunner_supportedmaps', Base.metadata,
   Column('botrunner_id', Integer,ForeignKey('botrunners.botrunner_id'),nullable = False),
   Column('map_id', Integer,ForeignKey('maps.map_id'),nullable = False),
   UniqueConstraint('botrunner_id', 'map_id' )
)

botrunner_supportedmods = Table( 'botrunner_supportedmods', Base.metadata,
   Column('botrunner_id', Integer,ForeignKey('botrunners.botrunner_id'),nullable = False),
   Column('mod_id', Integer,ForeignKey('mods.mod_id'),nullable = False),
   UniqueConstraint('botrunner_id', 'mod_id' )
)

botrunner_supportedais = Table( 'botrunner_supportedais', Base.metadata,
   Column('botrunner_id', Integer,ForeignKey('botrunners.botrunner_id'), nullable = False),
   Column('ai_id', Integer,ForeignKey('ais.ai_id'), nullable = False ),
   UniqueConstraint('botrunner_id', 'ai_id' )
)

botrunner_assignedoptions = Table( 'botrunner_assignedoptions', Base.metadata,
   Column('botrunner_id',Integer,ForeignKey('botrunners.botrunner_id'),nullable = False),
   Column('botrunner_option_id',Integer,ForeignKey('aioptions.option_id'),nullable = False),
   UniqueConstraint('botrunner_id','botrunner_option_id')
)

class BotRunner(Base):
   __tablename__ = 'botrunners'

   botrunner_id = Column(Integer,primary_key=True)
   botrunner_name = Column(String(255), unique = True, nullable = False)
   botrunner_sharedsecret = Column(String(255), nullable = False)
   botrunner_owneraccountid = Column(Integer, ForeignKey('accounts.account_id') )
   rowspan = 0 # used by viewbotrunners.py

   owneraccount = relationship("Account")
   options = relationship("AIOption", secondary = botrunner_assignedoptions )
   supportedmaps = relationship("Map", secondary = botrunner_supportedmaps )
   supportedmods = relationship("Mod", secondary = botrunner_supportedmods )
   supportedais = relationship("AI", secondary = botrunner_supportedais )
   sessions = relationship("BotRunnerSession",uselist = True)

   rowspan = 0

   def __init__( self, botrunner_name, botrunner_sharedsecret ):
      self.botrunner_name = botrunner_name
      self.botrunner_sharedsecret = botrunner_sharedsecret
