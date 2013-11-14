from base import *
from ai import AI
from mod_side import ModSide
from match_request import MatchRequest

class MatchRequestAI(Base):
    __tablename__ = 'match_request_ai'

    matchrequest_ai_id = Column(Integer, primary_key=True)

    matchrequest_id = Column(Integer, ForeignKey('matchrequest.matchrequest_id'), nullable=False)
    ai_id = Column(Integer, ForeignKey('ai.ai_id'), nullable=False)
    ai_side_id = Column(Integer, ForeignKey('mod_side.mod_side_id'),
            nullable=False)

    matchrequest = relationship("MatchRequest", primaryjoin=matchrequest_id == MatchRequest.matchrequest_id)
    ai = relationship("AI", primaryjoin=ai_id == AI.ai_id)
    ai_side = relationship("ModSide", primaryjoin=ai_side_id ==
            ModSide.mod_side_id)


    def __init__(self, ai, ai_side, match_request):
        self.ai = ai
        self.ai_side = ai_side
        self.match_request = match_request
