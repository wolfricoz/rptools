from typing import List
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy_utils import create_database, database_exists

from data.config import Config

from sqlalchemy import BigInteger, ForeignKey, Integer, NullPool, String, create_engine, JSON
engine = create_engine(Config().get_db_url(), echo=False, poolclass=NullPool)
if not database_exists(engine.url) :
	create_database(engine.url)

class Base(DeclarativeBase):
	pass

class User(Base):
	__tablename__ = "users"

	id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
	# Add other columns as needed

class Template(Base):
	__tablename__ = "templates"
	id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
	user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
	name: Mapped[str] = mapped_column(String(255))
	data: Mapped[str] = mapped_column(JSON)

class Character(Base):
	__tablename__ = "characters"
	id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
	user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
	prefix: Mapped[str] = mapped_column(String(255))
	name: Mapped[str] = mapped_column(String(255))
	character_info: Mapped[List["CharacterInfo"]] = relationship(back_populates="character")
	# Add other columns as needed

class CharacterInfo(Base):
	__tablename__ = "character_info"
	id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
	character_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("characters.id", ondelete="CASCADE"))
	key: Mapped[str] = mapped_column(String(255))
	value: Mapped[str] = mapped_column(String(4096))
	position: Mapped[int] = mapped_column(Integer)
	character: Mapped[Character] = relationship("Character", back_populates="character_info")
	# Add other columns as needed

def create_tables():
	"""Creates the tables in the database."""
	Base.metadata.create_all(engine)