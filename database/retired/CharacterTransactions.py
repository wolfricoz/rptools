from database.DatabaseTransactions import DatabaseTransactions
from database.UserTransactions import UserTransactions
from database.database import Character, CharacterInfo, Template


class CharacterTransactions(DatabaseTransactions):
	table = Character
	sub_table = CharacterInfo

	def get_character(self, character_id: int = None, user_id: int = None, name: str = None) -> Character | bool:
		"""Gets a template from the database."""
		if character_id:
			return self.session.query(self.table).join(self.sub_table).get(character_id)
		return self.session.query(self.table).filter_by(user_id=user_id, name=name).first()


	def count(self, user_id: int) -> int:
		"""Counts the number of templates for a user."""
		return self.session.query(self.table).filter_by(user_id=user_id).count()

	def delete(self, user_id: int, name: str) -> bool:
		"""Deletes a template from the database."""
		template = self.get_template(user_id=user_id, name=name)
		if template is None :
			return False
		self.session.delete(template)
		self.commit()
		return True

	def get(self, user_id: int) -> list:
		"""Gets all templates from the database."""
		pass

	def get_all(self, user_id: int) -> Character | dict:
		"""Gets all templates from the database."""
		characters = self.session.query(self.table).filter_by(user_id=user_id).all()
		if characters is None :
			return {}
		return characters

	def exists(self, user_id: int, name: str) -> bool:
		"""Checks if a template exists in the database."""
		return self.session.query(self.table).filter_by(user_id=user_id, name=name.lower()).first() is not None