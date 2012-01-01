from base import *

class League(Base):
    __tablename__ = 'league'

    league_id = Column(Integer, primary_key=True)
    league_name = Column(String(255), unique=True, nullable=False)
    league_creator_id = Column(Integer, ForeignKey('account.account_id'))
    map_id = Column(String(255), nullable=False)
    mod_id = Column(String(255), nullable=False)
    matches_per_ai_pair = Column(Integer, nullable=False)
    speed = Column(Integer, nullable=False)
    soft_timeout = Column(Integer, nullable=False)
    hard_timeout = Column(Integer, nullable=False)
    #ugly but allows for different modes easily
    sides = Column(String(255), nullable=False)
    side_modes = Column(String(255), nullable=False)
    play_against_self = Column(Boolean, nullable=False)

    creator = relationship("Account")
    league_ais = relationship("LeagueAI")

    def __init__(self, league_name, creator, mod_id, map_id,
            matches_per_ai_pair, speed, soft_timeout, hard_timeout, sides,
            side_modes, play_against_self):
        self.league_name = league_name
        self.creator = creator
        self.mod_id = mod_id
        self.map_id = map_id
        self.matches_per_ai_pair = matches_per_ai_pair
        self.speed = speed
        self.soft_timeout = soft_timeout
        self.hard_timeout = hard_timeout
        self.sides = sides
        self.side_modes = side_modes
        self.play_against_self = play_against_self
