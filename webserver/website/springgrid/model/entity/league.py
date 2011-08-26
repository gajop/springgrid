from base import *

league_options = Table('league_options', Base.metadata,
   Column('league_id', Integer, ForeignKey('leagues.league_id'),
       nullable=False),
   Column('option_id', Integer, ForeignKey('aioptions.option_id'),
       nullable=False),
   UniqueConstraint('league_id', 'option_id')
)


class League(Base):
    __tablename__ = 'leagues'

    league_id = Column(Integer, primary_key=True)
    league_name = Column(String(255), unique=True, nullable=False)
    league_creatorid = Column(Integer, ForeignKey('accounts.account_id'))
    map_id = Column(String(255), nullable=False)
    mod_id = Column(String(255), nullable=False)
    nummatchesperaipair = Column(Integer, nullable=False)
    speed = Column(Integer, nullable=False)
    softtimeout = Column(Integer, nullable=False)
    hardtimeout = Column(Integer, nullable=False)
    #ugly but allows for different modes easily
    sides = Column(String(255), nullable=False)
    sidemodes = Column(String(255), nullable=False)
    playagainstself = Column(Boolean, nullable=False)

    creator = relationship("Account")
    options = relationship("AIOption", secondary=league_options)
    league_ais = relationship("LeagueAI")

    def __init__(self, league_name, creator, mod_id, map_id,
            nummatchesperaipair, speed, softtimeout, hardtimeout, sides,
            sidemodes, playagainstself):
        self.league_name = league_name
        self.creator = creator
        self.mod_id = mod_id
        self.map_id = map_id
        self.nummatchesperaipair = nummatchesperaipair
        self.speed = speed
        self.softtimeout = softtimeout
        self.hardtimeout = hardtimeout
        self.sides = sides
        self.sidemodes = sidemodes
        self.playagainstself = playagainstself
