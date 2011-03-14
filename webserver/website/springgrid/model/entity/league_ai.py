from base import *
from league import League

class LeagueAI(Base):
    __tablename__ = "league_ais"
    league_ai_id = Column(Integer, primary_key=True)
    #sadly not a foreign key since AIs aren't added at the right time yet...
    ai_id = Column(Integer, nullable=False)
    league_id = Column(Integer, ForeignKey('leagues.league_id'),
            nullable=False)

    league = relationship("League", primaryjoin=league_id == League.league_id)

    def __init__(self, ai_id, league):
        self.ai_id = ai_id
        self.league = league
