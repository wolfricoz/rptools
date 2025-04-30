from database.DatabaseTransactions import DatabaseTransactions
from database.UserTransactions import UserTransactions
from database.database import Template


class TemplateTransactions(DatabaseTransactions):
	table = Template

	def create_template(self, user_id: int, name: str, data: str) -> Template | bool:
		"""Creates a new template in the database."""
		name = name.lower()
		if UserTransactions().exists(user_id) is False:
			UserTransactions().create_user(user_id)
		if self.exists(user_id, name):
			return False
		template = self.table(user_id=user_id, name=name, data=data)
		self.session.add(template)
		self.commit()
		return template

	def get_template(self, user_id: int, name: str) -> Template | bool:
		"""Gets a template from the database."""
		return self.session.query(self.table).filter_by(user_id=user_id, name=name).first()


	def count_templates(self, user_id: int) -> int:
		"""Counts the number of templates for a user."""
		return self.session.query(self.table).filter_by(user_id=user_id).count()

	def delete_template(self, user_id: int, name: str) -> bool:
		"""Deletes a template from the database."""
		template = self.get_template(user_id=user_id, name=name)
		if template is None :
			return False
		self.session.delete(template)
		self.commit()
		return True

	def get_all_templates(self, user_id: int) -> list:
		"""Gets all templates from the database."""
		templates = self.session.query(self.table).filter_by(user_id=user_id).all()
		if templates is None :
			return []
		return [template.name for template in templates]

	def exists(self, user_id: int, name: str) -> bool:
		"""Checks if a template exists in the database."""
		return self.session.query(self.table).filter_by(user_id=user_id, name=name).first() is not None