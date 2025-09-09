import os

from dotenv import load_dotenv
load_dotenv(".env")
class Config():
	"""Configuration for the bot, loads the environment variables and sets up the database connection."""


	Config = {
		"TOKEN": os.getenv("TOKEN"),
		"PREFIX": os.getenv("PREFIX", default="!"),
		"DATABASE_NAME": os.getenv("DATABASE_NAME", default="rpcrafter"),
		"DATABASE_USER": os.getenv("DATABASE_USER", default="root"),
		"DATABASE_PASSWORD": os.getenv("DATABASE_PASSWORD", default=""),
		"DATABASE_HOST": os.getenv("DATABASE_HOST", default="localhost"),
		"DATABASE_PORT": os.getenv("DATABASE_PORT", default=3306),
	}

	def get_db_url(self):
		"""Returns the database URL for SQLAlchemy."""
		return f"postgresql+psycopg2://{self.Config['DATABASE_USER']}:{self.Config['DATABASE_PASSWORD']}@{self.Config['DATABASE_HOST']}:{self.Config['DATABASE_PORT']}/{self.Config['DATABASE_NAME']}"
