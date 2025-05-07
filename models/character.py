import logging
from typing import Self

from database.DatabaseTransactions import DatabaseTransactions
from database.UserTransactions import UserTransactions
from database.database import Character as CharacterDB
from database.database import CharacterInfo


class Character(DatabaseTransactions) :
	table: CharacterDB = CharacterDB
	sub_table: CharacterInfo = CharacterInfo

	def __init__(self, id: int = 0) :
		self.character_info = {}
		self.id = id
		logging.info(f"character id: {id}")
		data: CharacterDB = self.get_character(character_id=id)
		logging.info(f"character data: {data}")
		self.set_character_data(data)

	def __int__(self) :
		return self.id

	def get_all_character_info(self) :
		"""Gets all character info from the database."""
		return {f"{info.key}": {"value": info.value, "position": info.position } for info in self.session.query(self.sub_table).filter_by(character_id=self.id).all()}

	def add_character_info(self, key: str, value: str) -> Self :
		"""Adds character info to the database."""
		existing_character_info = self.get_all_character_info()
		if key in existing_character_info :
			return None

		pos = len(existing_character_info) + 1
		character_data = CharacterInfo(character_id=self.id, key=key, value=value, position=pos)
		self.session.add(character_data)
		self.commit()
		logging.info(f"added character info: {key} to {character_data}")
		existing_character_info[key] = {"value" : value, "position" : pos}
		self.character_info = existing_character_info
		return self

	def remove_character_info(self, key: str) -> Self :
		"""Removes character info from the database."""
		existing_character_info = self.get_all_character_info()
		if key not in existing_character_info :
			return None
		character_data = self.session.query(self.sub_table).filter_by(character_id=self.id, key=key).first()
		self.session.delete(character_data)
		self.commit()
		logging.info(f"removed character info: {key} from {character_data}")
		del existing_character_info[key]
		self.character_info = existing_character_info
		return self

	def edit_character_info(self, key: str, value: str) -> Self :
		"""Edits character info in the database."""
		existing_character_info = self.get_all_character_info()
		if key not in existing_character_info :
			return None
		character_data = self.session.query(self.sub_table).filter_by(character_id=self.id, key=key).first()
		character_data.value = value
		self.session.commit()
		logging.info(f"edited character info: {key} to {character_data}")
		existing_character_info[key] = value
		self.character_info = existing_character_info
		return self

	def change_character_info_position(self, key: str, position: int) -> Self :
		"""Changes the position of character info in the database."""
		existing_character_info = self.get_all_character_info()
		if key not in existing_character_info :
			return None
		for k, v in existing_character_info.items() :
			if v == position :
				existing_character_info[k] = existing_character_info[key]

		character_data = self.session.query(self.sub_table).filter_by(character_id=self.id, key=key).first()
		character_data.position = position
		self.session.commit()
		logging.info(f"changed character info position: {key} to {character_data}")
		self.character_info = existing_character_info
		return self

	def set_character_data(self, data: CharacterDB) :
		self.id = data.id if data is not None else 0
		self.name = data.name if data is not None else None
		self.prefix = data.prefix if data is not None else None
		self.user_id = data.user_id if data is not None else None
		self.character_info = self.get_all_character_info()

	# Transactional methods
	def create(self, user_id: int, name: str, prefix: str) -> Self | None :
		"""Creates a new template in the database."""
		name = name.lower()
		prefix = prefix.lower()
		if UserTransactions().exists(user_id) is False :
			UserTransactions().create_user(user_id)
		if self.exists(user_id, name) :
			return None
		character = self.table(user_id=user_id, name=name, prefix=prefix)
		self.session.add(character)
		self.commit()
		self.set_character_data(character)

		return self

	def get_character(self, character_id: int = None, user_id: int = None, name: str = None) -> CharacterDB | bool :
		"""Gets a template from the database."""
		if character_id :
			# Use filter instead of get() when additional criteria are involved
			return self.session.query(self.table).filter(self.table.id == character_id).outerjoin(self.sub_table).first()
		return self.session.query(self.table).filter_by(user_id=user_id, name=name).first()

	def count(self, user_id: int) -> int :
		"""Counts the number of templates for a user."""
		return self.session.query(self.table).filter_by(user_id=user_id).count()

	def delete(self) -> bool :
		"""Deletes a template from the database."""
		character = self.get_character(character_id=self.id)
		if character is None :
			return False
		self.session.delete(character)
		self.commit()
		return True

	def get(self, user_id: int) -> list :
		"""Gets all templates from the database."""
		pass

	def get_all(self, user_id: int) -> CharacterDB | dict :
		"""Gets all templates from the database."""
		characters = self.session.query(self.table).filter_by(user_id=user_id).all()
		if characters is None :
			return {}
		return characters

	def exists(self, user_id: int, name: str) -> bool :
		"""Checks if a template exists in the database."""
		return self.session.query(self.table).filter_by(user_id=user_id, name=name.lower()).first() is not None


