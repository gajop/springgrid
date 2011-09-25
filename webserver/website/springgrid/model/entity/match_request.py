from base import *
from ai import AI
from mod_side import ModSide

matchrequest_options = Table('matchrequest_options', Base.metadata,
   Column('matchrequest_id', Integer,
       ForeignKey('matchrequestqueue.matchrequest_id'), nullable=False),
   Column('option_id', Integer, ForeignKey('aioptions.option_id'),
       nullable=False),
   UniqueConstraint('matchrequest_id', 'option_id')
)


class MatchRequest(Base):
    __tablename__ = 'matchrequestqueue'

    matchrequest_id = Column(Integer, primary_key=True)
    map_id = Column(Integer, ForeignKey('maps.map_id'), nullable=False)
    league_id = Column(Integer, ForeignKey('leagues.league_id'), nullable=True)
    mod_id = Column(Integer, ForeignKey('mods.mod_id'), nullable=False)
    ai0_id = Column(Integer, ForeignKey('ais.ai_id'), nullable=False)
    ai0_side_id = Column(Integer, ForeignKey('mod_sides.mod_side_id'),
            nullable=False)
    ai1_id = Column(Integer, ForeignKey('ais.ai_id'), nullable=False)
    ai1_side_id = Column(Integer, ForeignKey('mod_sides.mod_side_id'),
            nullable=False)
    speed = Column(Integer, nullable=False)
    softtimeout = Column(Integer, nullable=False)
    hardtimeout = Column(Integer, nullable=False)

    map = relationship("Map")
    mod = relationship("Mod")
    ai0 = relationship("AI", primaryjoin=ai0_id == AI.ai_id)
    ai1 = relationship("AI", primaryjoin=ai1_id == AI.ai_id)
    ai0_side = relationship("ModSide", primaryjoin=ai0_side_id ==
            ModSide.mod_side_id)
    ai1_side = relationship("ModSide", primaryjoin=ai1_side_id ==
            ModSide.mod_side_id)
    league = relationship("League")
    matchrequestinprogress = relationship("MatchRequestInProgress",
            uselist=False)
    matchresult = relationship("MatchResult", uselist=False)
    options = relationship("AIOption", secondary=matchrequest_options)

    def __init__(self, ai0, ai1, map, mod, speed, softtimeout, hardtimeout,
            ai0_side, ai1_side, league_id = None):
        self.ai0 = ai0
        self.ai1 = ai1
        self.map = map
        self.mod = mod
        self.speed = speed
        self.softtimeout = softtimeout
        self.hardtimeout = hardtimeout
        self.ai0_side = ai0_side
        self.ai1_side = ai1_side
        self.league_id = league_id
        
