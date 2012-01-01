from base import *

ai_allowedmaps = Table('ai_allowedmap', Base.metadata,
   Column('ai_id', Integer, ForeignKey('ai.ai_id'), 
       nullable=False),
   Column('map_id', Integer, ForeignKey('map.map_id'), nullable=False),
   UniqueConstraint('ai_id', 'map_id')
)

ai_allowedmods = Table('ai_allowedmod', Base.metadata,
   Column('ai_id', Integer, ForeignKey('ai.ai_id'), 
       nullable=False),
   Column('mod_id', Integer, ForeignKey('mod.mod_id'), nullable=False),
   UniqueConstraint('ai_id', 'mod_id')
)

ai_allowedoptions = Table('ai_allowedoption', Base.metadata,
   Column('ai_id', Integer, ForeignKey('ai.ai_id'), 
       nullable=False),
   Column('option_id', Integer, ForeignKey('aioption.option_id'),
       nullable=False),
   UniqueConstraint('ai_id', 'option_id')
)

class AI(Base):
    __tablename__ = 'ai'

    ai_id = Column(Integer, primary_key=True)
    ai_version = Column(String(64), nullable=False)
    ai_downloadurl = Column(String(255))
    ai_needscompiling = Column(Boolean)
    ai_base_id = Column(Integer, ForeignKey('ai_base.ai_base_id'), nullable=False)

    __table_args__ = (schema.UniqueConstraint('ai_base_id', 'ai_version'), {})

    allowedmaps = relationship("Map", secondary=ai_allowedmaps)
    allowedmods = relationship("Mod", secondary=ai_allowedmods)
    allowedoptions = relationship("AIOption", secondary=ai_allowedoptions)

    def __init__(self, ai_base_id, ai_version):
        self.ai_version = ai_version
        self.ai_base_id = ai_base_id
