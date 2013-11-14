from base import *
from ai import AI
from mod_side import ModSide
from match_configuration import MatchConfiguration

class MatchConfigurationAI(Base):
    __tablename__ = 'matchconfiguration_ai'

    matchconfiguration_ai_id = Column(Integer, primary_key=True)

    matchconfiguration_id = Column(Integer, ForeignKey('matchconfiguration.matchconfiguration_id'), nullable=False)
    ai_id = Column(Integer, ForeignKey('ai.ai_id'), nullable=False)
    ai_side_id = Column(Integer, ForeignKey('mod_side.mod_side_id'),
            nullable=False)

    matchconfiguration = relationship("MatchConfiguration", primaryjoin=matchconfiguration_id == MatchConfiguration.matchconfiguration_id)
    ai = relationship("AI", primaryjoin=ai_id == AI.ai_id)
    ai_side = relationship("ModSide", primaryjoin=ai_side_id ==
            ModSide.mod_side_id)


    def __init__(self, ai, ai_side, match_configuration):
        self.ai = ai
        self.ai_side = ai_side
        self.match_configuration = match_configuration
