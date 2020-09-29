from server_api import ServerApi
from models import User


class Analizer:
	def __init__(self, event):
		self.api = ServerApi() 
		self.user_id = event.user_id
		self.event = event
	
	def add_user_if_not_exist(self):
		if self.api.request('user_is_exist', event.user_id):
			self.api.request('add_user', event.user_id)
		query = self.user.select().where(User.user_id==self.user_id)
		if list(query) == 0:
			self.user.create(user_id=user_id, status='setup')
		return True

	def set_user_model(self):
		self.user = User.get(User.user_id==self.user_id)

	def check_user_status(self):
		user = User.get(User.user_id==self.user_id)

