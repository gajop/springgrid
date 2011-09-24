from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, String, Integer, Boolean, DateTime, \
        ForeignKey, and_, schema, Table, UniqueConstraint
from sqlalchemy.orm import backref, relationship

# The declarative Base
Base = declarative_base()
