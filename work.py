from config import vk
import random
from chain import give_chain


class Work:
	def __init__(self):
		self.vk = vk
		self.chain = give_chain()
		self.message = dict()

	def set_event(self, event):
		self.event = event

	def main(self):
		self.update_params_for_new_user()
		self.analize()
		self.send_message()

	def update_params_for_new_user(self):
		self.message['user_id'] = self.event.user_id
		self.message['message'] = ''
		self.message['attachments'] = ''
		self.message['random_id'] = random.randint(1, 2 ** 32)
		self.message['keyboard'] = ''

	def analize(self):
		self.event.text = self.event.text.lower()
		data = self.chain.handle(self.event)
		print(data)
		if 'message' in data:
			self.message['message'] = data['message']
		if 'keyboard' in data:
			self.message['keyboard'] = data['keyboard']
		if 'attachments' in data:
			self.message['attachments'] = data['attachments']

	def send_message(self):
		self.vk.messages.send(**self.message)
