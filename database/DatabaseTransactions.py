from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from database.database import engine


class ConfigNotFound(Exception) :
	"""config item was not found or has not been added yet."""

	def __init__(self, message="guild config has not been loaded yet or has not been created yet.") :
		self.message = message
		super().__init__(self.message)


class CommitError(Exception) :
	"""the commit failed."""

	def __init__(self, message="Commiting the data to the database failed and has been rolled back; please try again.") :
		self.message = message
		super().__init__(self.message)


class KeyNotFound(Exception) :
	"""config item was not found or has not been added yet."""

	def __init__(self, key) :
		self.key = key
		self.message = f"`{key}` not found in config, please add it using /config"
		super().__init__(self.message)


class DatabaseTransactions :
	session = Session(bind=engine, expire_on_commit=False)

	def commit(self) :
		try :
			self.session.commit()
		except SQLAlchemyError as e :
			print(e)
			self.session.rollback()
			raise CommitError()
		finally :
			self.session.close()

	def refresh(self) :
		self.session.expire_all()

	def truncate(self, table: str) :
		if table not in ['proof'] :
			return False

		self.session.execute(text(f"TRUNCATE TABLE {table}"))
		self.commit()