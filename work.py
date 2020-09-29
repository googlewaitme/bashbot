from config import vk
import random
from analizer import Analizer


analizer = Analizer()


class Work:
	def __init__(self):
		self.vk = vk
		self.message = dict()

	def set_event(self, event):
		self.event = event

	def main(self):
		self.update_params_for_new_user()
		self.analize()
		self.send_requst()
		self.send_message()

	def update_params_for_new_user(self):
		self.message['user_id'] = self.event.user_id
		self.message['message'] = ''
		self.message['attachments'] = list()
		self.message['random_id'] = random.randint(1, 2 ** 32)
		self.message['keyboard'] = ''

	def analize(self):
		analizer(self.event)

	def send_message(self):
		self.vk.messages.send(**self.message)
