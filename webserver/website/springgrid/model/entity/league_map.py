from base import *
from league import League

#maps that are being used in a league
class LeagueMap(Base):
    __tablename__ = "league_map"
    league_map_id = Column(Integer, primary_key=True)
    map_id = Column(Integer, ForeignKey('map.map_id'), nullable=False)
    league_id = Column(Integer, ForeignKey('league.league_id'),
            nullable=False)

    league = relationship("League", primaryjoin=league_id == League.league_id)

    def __init__(self, map_id, league):
        self.map_id = map_id
        self.league = league
