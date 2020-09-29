from peewee import *


database = SqliteDatabase('bash.db')


def create_tables(with_drop=False):
	global database
	models = [User]
	for model in models:
		if with_drop:
			model.drop_table()
		model.create_table()


class BaseModel(Model):
	class Meta:
		database = database


class User(BaseModel):
	user_id = CharField(unique=True, null=False)
	user_answer = TextField(null=False)
	question_id = IntegerField(null=False)
	status = CharField()
