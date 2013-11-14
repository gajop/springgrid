from base import *
from mod_side import ModSide

class MatchConfiguration(Base):
    __tablename__ = 'matchconfiguration'

    matchconfiguration_id = Column(Integer, primary_key=True)
    engine_id = Column(Integer, ForeignKey('engine.engine_id'), nullable=False)
    map_id = Column(Integer, ForeignKey('map.map_id'), nullable=False)
    mod_id = Column(Integer, ForeignKey('mod.mod_id'), nullable=False)
    speed = Column(Integer, nullable=False)
    softtimeout = Column(Integer, nullable=False)
    hardtimeout = Column(Integer, nullable=False)

    engine = relationship("Engine")
    map = relationship("Map")
    mod = relationship("Mod")

    def __init__(self, map, mod, speed, softtimeout, hardtimeout, engine):
        self.map = map
        self.mod = mod
        self.speed = speed
        self.softtimeout = softtimeout
        self.hardtimeout = hardtimeout
        self.engine = engine
