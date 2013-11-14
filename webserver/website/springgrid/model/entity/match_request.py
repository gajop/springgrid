from base import *
from mod_side import ModSide

class MatchRequest(Base):
    __tablename__ = 'matchrequest'

    matchrequest_id = Column(Integer, primary_key=True)
    league_id = Column(Integer, ForeignKey('league.league_id'), nullable=True)
    match_configuration_id = Column(Integer, ForeignKey('matchconfiguration.matchconfiguration_id'), nullable=False)

    match_configuration = relationship("MatchConfiguration")
    league = relationship("League")
    matchrequestinprogress = relationship("MatchRequestInProgress",
            uselist=False)
    matchresult = relationship("MatchResult", uselist=False)

    def __init__(self, match_configuration_id, league_id = None):
        self.match_configuration_id = match_configuration_id
        self.league_id = league_id
