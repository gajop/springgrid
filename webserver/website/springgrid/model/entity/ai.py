from base import *

ai_allowedmaps = Table('ai_allowedmaps', Base.metadata,
   Column('ai_id', Integer, ForeignKey('ais.ai_id'), nullable=False),
   Column('map_id', Integer, ForeignKey('maps.map_id'), nullable=False),
   UniqueConstraint('ai_id', 'map_id')
)

ai_allowedmods = Table('ai_allowedmods', Base.metadata,
   Column('ai_id', Integer, ForeignKey('ais.ai_id'), nullable=False),
   Column('mod_id', Integer, ForeignKey('mods.mod_id'), nullable=False),
   UniqueConstraint('ai_id', 'mod_id')
)

ai_allowedoptions = Table('ai_allowedoptions', Base.metadata,
   Column('ai_id', Integer, ForeignKey('ais.ai_id'), nullable=False),
   Column('option_id', Integer, ForeignKey('aioptions.option_id'),
       nullable=False),
   UniqueConstraint('ai_id', 'option_id')
)


class AI(Base):
    __tablename__ = 'ais'

    ai_id = Column(Integer, primary_key=True)
    ai_name = Column(String(64), nullable=False)
    ai_version = Column(String(64), nullable=False)
    ai_downloadurl = Column(String(255))
    ai_needscompiling = Column(Boolean)
    ai_owneraccount_id = Column(Integer, ForeignKey('accounts.account_id'))

    __table_args__ = (schema.UniqueConstraint('ai_name', 'ai_version'), {})

    allowedmaps = relationship("Map", secondary=ai_allowedmaps)
    allowedmods = relationship("Mod", secondary=ai_allowedmods)
    allowedoptions = relationship("AIOption", secondary=ai_allowedoptions)

    owneraccount = relationship("Account")

    def __init__(self, ai_name, ai_version):
        self.ai_name = ai_name
        self.ai_version = ai_version
        self.needscompiling = True
