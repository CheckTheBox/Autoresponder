import logging
from sqlalchemy import Column
from sqlalchemy import Integer, BigInteger, String
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection

# import utils

log = logging.getLogger(__name__)

# Create a base class to define all the database subclasses
TableDeclarativeBase = declarative_base()


# Define all the database tables using the sqlalchemy declarative base
class User(DeferredReflection, TableDeclarativeBase):
    """A Telegram user who used the bot at least once."""

    # Telegram data
    user_id = Column(BigInteger, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    username = Column(String)
    phone_number = Column(String, default=None)

    # Extra table parameters
    __tablename__ = "users"
