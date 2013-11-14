from base import *
from mod_side import ModSide

class MatchRequest(Base):
    __tablename__ = 'matchrequest'

    matchrequest_id = Column(Integer, primary_key=True)
    engine_id = Column(Integer, ForeignKey('engine.engine_id'), nullable=False)
    map_id = Column(Integer, ForeignKey('map.map_id'), nullable=False)
    league_id = Column(Integer, ForeignKey('league.league_id'), nullable=True)
    mod_id = Column(Integer, ForeignKey('mod.mod_id'), nullable=False)
    speed = Column(Integer, nullable=False)
    softtimeout = Column(Integer, nullable=False)
    hardtimeout = Column(Integer, nullable=False)

    engine = relationship("Engine")
    map = relationship("Map")
    mod = relationship("Mod")
    league = relationship("League")
    matchrequestinprogress = relationship("MatchRequestInProgress",
            uselist=False)
    matchresult = relationship("MatchResult", uselist=False)

    def __init__(self, map, mod, speed, softtimeout, hardtimeout, engine, league_id = None):
        self.map = map
        self.mod = mod
        self.speed = speed
        self.softtimeout = softtimeout
        self.hardtimeout = hardtimeout
        self.league_id = league_id
        self.engine = engine
