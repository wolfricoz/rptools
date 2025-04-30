import pymysql
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy_utils import create_database, database_exists

from data.config import Config

pymysql.install_as_MySQLdb()
from sqlalchemy import BigInteger, ForeignKey, String, create_engine, JSON
engine = create_engine(Config().get_db_url(), echo=True)
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


def create_tables():
	"""Creates the tables in the database."""
	Base.metadata.create_all(engine)