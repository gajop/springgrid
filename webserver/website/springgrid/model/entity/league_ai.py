from base import *
from league import League

#ais that are being used in a league
class LeagueAI(Base):
    __tablename__ = "league_ai"
    league_ai_id = Column(Integer, primary_key=True)
    ai_id = Column(Integer, ForeignKey('ai.ai_id'), nullable=False)
    league_id = Column(Integer, ForeignKey('league.league_id'),
            nullable=False)

    league = relationship("League", primaryjoin=league_id == League.league_id)

    def __init__(self, ai_id, league):
        self.ai_id = ai_id
        self.league = league
