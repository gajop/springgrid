from base import *

class AIBase(Base):
    __tablename__ = 'ai_base'

    ai_base_id = Column(Integer, primary_key=True)
    ai_base_name = Column(String(64), nullable=False)
    ai_base_owneraccount_id = Column(Integer, ForeignKey('account.account_id'))

    owneraccount = relationship("Account")
    versions = relationship("AI", backref='ai_base', uselist=True)

    def __init__(self, ai_base_name):
        self.ai_base_name = ai_base_name
        self.needscompiling = True
