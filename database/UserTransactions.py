from sqlalchemy import Select, exists

from database.DatabaseTransactions import DatabaseTransactions
from database.database import User


class UserTransactions(DatabaseTransactions):
	table = User
	def create_user(self, user_id: int) -> User:
		"""Creates a new user in the database."""
		user = self.table(id=user_id)
		self.session.add(user)
		self.commit()
		return user

	def exists(self, user_id: int) -> User:
		return self.session.query(exists().where(self.table.id == user_id)).scalar()