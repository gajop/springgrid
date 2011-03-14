from base import *


class AIOption(Base):
    __tablename__ = 'aioptions'

    option_id = Column(Integer, primary_key=True)
    option_name = Column(String(255), unique=True, nullable=False)

    def __init__(self, option_name):
        self.option_name = option_name

